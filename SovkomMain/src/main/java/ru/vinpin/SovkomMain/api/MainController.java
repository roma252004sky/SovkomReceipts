package ru.vinpin.SovkomMain.api;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import ru.vinpin.SovkomMain.dto.ClickHouseReceiptDTO;
import ru.vinpin.SovkomMain.dto.ItemDTO;
import ru.vinpin.SovkomMain.dto.ReceiptDTO;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api")
public class MainController {

    private final WebClient clickHouseClient;
    private final ObjectMapper objectMapper;

    public MainController(WebClient clickHouseClient) {
        this.clickHouseClient = clickHouseClient;
        this.objectMapper = new ObjectMapper();
        this.objectMapper.registerModule(new JavaTimeModule());
    }

    @GetMapping("/getAll")
    public Flux<ReceiptDTO> getAll() {
        String query = "SELECT category, load_id, user_id, shop, total, date, items_json FROM core.history ORDER BY date DESC";

        return clickHouseClient.get()
                .uri(uriBuilder -> uriBuilder
                        .queryParam("query", query)
                        .queryParam("default_format", "JSONEachRow")
                        .build())
                .retrieve()
                .bodyToFlux(String.class)
                .flatMap(this::parseReceipt);
    }

    @GetMapping("/getFirst3")
    public Flux<ReceiptDTO> getFirst3() {
        String query = "SELECT category, load_id, user_id, shop, total, date, items_json FROM core.history ORDER BY date DESC LIMIT 3";

        return clickHouseClient.get()
                .uri(uriBuilder -> uriBuilder
                        .queryParam("query", query)
                        .queryParam("default_format", "JSONEachRow")
                        .build())
                .retrieve()
                .bodyToFlux(String.class)
                .flatMap(this::parseReceipt);
    }

    private Mono<ReceiptDTO> parseReceipt(String json) {
        return Mono.fromCallable(() -> objectMapper.readValue(json, ClickHouseReceiptDTO.class))
                .flatMap(receipt -> {
                    List<ItemDTO> items = new ArrayList<>();
                    try {
                        items = objectMapper.readValue(receipt.getItems_json(), new TypeReference<>() {
                        });
                    } catch (JsonProcessingException e) {
                    }
                    ReceiptDTO receiptDTO = new ReceiptDTO();
                    receiptDTO.setCategory(receipt.getCategory());
                    receiptDTO.setDate(receipt.getDate());
                    receiptDTO.setTotal(receipt.getTotal());
                    receiptDTO.setItems(items);
                    receiptDTO.setShop(receipt.getShop());
                    receiptDTO.setLoadId(receipt.getLoad_id().toString());
                    receiptDTO.setUserId(receipt.getUser_id());

                    return Mono.just(receiptDTO);
                })
                .onErrorResume(e -> {
                    System.err.println("Error parsing receipt: " + e.getMessage());
                    return Mono.empty();
                });
    }
}