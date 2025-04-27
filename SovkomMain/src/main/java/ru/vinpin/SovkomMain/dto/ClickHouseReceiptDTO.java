package ru.vinpin.SovkomMain.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

public class ClickHouseReceiptDTO {
    private String category;
    private UUID load_id;
    private String user_id;
    private String shop;
    private BigDecimal total;
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime date;
    private String items_json;
    public ClickHouseReceiptDTO(){}
    public ClickHouseReceiptDTO(ReceiptDTO original, ObjectMapper mapper) throws JsonProcessingException {
        this.category = original.getCategory();
        this.load_id = UUID.fromString(original.getLoadId());
        this.user_id = original.getUserId();
        this.shop = original.getShop();
        this.total = original.getTotal();
        this.date = original.getDate();
        this.items_json = mapper.writeValueAsString(original.getItems());
    }

    public ClickHouseReceiptDTO(String category, UUID load_id, String user_id, String shop, BigDecimal total, LocalDateTime date, String items_json) {
        this.category = category;
        this.load_id = load_id;
        this.user_id = user_id;
        this.shop = shop;
        this.total = total;
        this.date = date;
        this.items_json = items_json;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public UUID getLoad_id() {
        return load_id;
    }

    public void setLoad_id(UUID load_id) {
        this.load_id = load_id;
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public String getShop() {
        return shop;
    }

    public void setShop(String shop) {
        this.shop = shop;
    }

    public BigDecimal getTotal() {
        return total;
    }

    public void setTotal(BigDecimal total) {
        this.total = total;
    }

    public LocalDateTime getDate() {
        return date;
    }

    public void setDate(LocalDateTime date) {
        this.date = date;
    }

    public String getItems_json() {
        return items_json;
    }

    public void setItems_json(String items_json) {
        this.items_json = items_json;
    }

}
