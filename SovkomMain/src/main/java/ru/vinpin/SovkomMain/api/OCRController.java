package ru.vinpin.SovkomMain.api;

import org.apache.kafka.clients.producer.ProducerRecord;
import org.springframework.core.io.buffer.DataBufferUtils;
import org.springframework.http.MediaType;
import org.springframework.http.codec.multipart.FilePart;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

@RestController
@RequestMapping("/api")
public class OCRController {
    private final ReactiveKafkaProducerTemplate<String, byte[]> kafkaTemplate;

    public OCRController(ReactiveKafkaProducerTemplate<String, byte[]> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<String> uploadImage(
            @RequestPart("file") FilePart filePart,
            @RequestPart("userId") String userId) {

        return DataBufferUtils.join(filePart.content())
                .flatMap(dataBuffer -> {
                    try {
                        ByteBuffer byteBuffer = dataBuffer.asByteBuffer();
                        byteBuffer.rewind();
                        byte[] bytes = new byte[byteBuffer.remaining()];
                        byteBuffer.get(bytes);

                        int partition = ThreadLocalRandom.current().nextInt(16);

                        ProducerRecord<String, byte[]> record = new ProducerRecord<>(
                                "preOCR",
                                partition,
                                null,
                                bytes
                        );
                        record.headers().add("userId", userId.getBytes(StandardCharsets.UTF_8));
                        record.headers().add("loadId", UUID.randomUUID().toString().getBytes(StandardCharsets.UTF_8));
                        return kafkaTemplate.send(record)
                                .thenReturn("Sent to partition " + partition);
                    } finally {
                        DataBufferUtils.release(dataBuffer);
                    }
                });
    }
}
