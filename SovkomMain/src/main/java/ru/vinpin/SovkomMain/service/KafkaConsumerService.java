package ru.vinpin.SovkomMain.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.context.annotation.Bean;
import org.springframework.http.MediaType;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import reactor.kafka.receiver.ReceiverOptions;
import reactor.kafka.receiver.ReceiverRecord;
import jakarta.annotation.PostConstruct;
import ru.vinpin.SovkomMain.dto.ClickHouseReceiptDTO;
import ru.vinpin.SovkomMain.dto.ReceiptDTO;

import java.util.List;

@Service
public class KafkaConsumerService {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final ReactiveKafkaConsumerTemplate<String, byte[]> consumer;
    private final WebClient webClient;

    public KafkaConsumerService(
            ReceiverOptions<String, byte[]> receiverOptions,
            WebClient webClient
    ) {
        this.consumer = new ReactiveKafkaConsumerTemplate<>(receiverOptions.subscription(List.of("postOCR")));
        this.webClient = webClient;
        objectMapper.registerModule(new JavaTimeModule());
    }

    @PostConstruct
    public void startListening() {
        int partitionsPerInstance = 4;
        consumer.receive()
                .parallel(partitionsPerInstance)
                .runOn(Schedulers.parallel())
                .flatMap(this::processRecord)
                .subscribe();
    }

    private Mono<Void> processRecord(ReceiverRecord<String, byte[]> record) {
        return Mono.fromCallable(() -> {
                    String json = new String(record.value());
                    return objectMapper.readValue(json, ReceiptDTO.class);
                })
                .flatMap(dto -> {
                            try {
                                return sendToClickHouse(dto)
                                        .then(record.receiverOffset().commit());
                            } catch (JsonProcessingException e) {
                                throw new RuntimeException(e);
                            }
                        }
                )
                .onErrorResume(e -> {
                    System.err.println("Error processing record: " + e.getMessage());
                    return record.receiverOffset().commit();
                });
    }

    private Mono<Void> sendToClickHouse(ReceiptDTO dto) throws JsonProcessingException {
        String insertQuery = "INSERT INTO core.history FORMAT JSONEachRow";

        return webClient.post()
                .uri("http://clickhouse-server:8123/?query=" + insertQuery)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(new ClickHouseReceiptDTO(dto,objectMapper))
                .retrieve()
                .onStatus(status -> status.isError(), response ->
                        response.bodyToMono(String.class)
                                .flatMap(error -> Mono.error(new RuntimeException("ClickHouse error: " + error)))
                )
                .toBodilessEntity()
                .then();
    }
}