package ru.vinpin.SovkomMain;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class SovkomMainApplication {

	public static void main(String[] args) {
		SpringApplication.run(SovkomMainApplication.class, args);
	}

}
