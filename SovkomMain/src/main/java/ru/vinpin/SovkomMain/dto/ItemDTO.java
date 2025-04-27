package ru.vinpin.SovkomMain.dto;


import java.math.BigDecimal;

public class ItemDTO {
    private String name;
    private BigDecimal price;
    private int count;
    private BigDecimal total;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }

    public int getCount() { return count; }
    public void setCount(int count) { this.count = count; }

    public BigDecimal getTotal() { return total; }
    public void setTotal(BigDecimal total) { this.total = total; }
}
