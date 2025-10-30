package com.example;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.main.Main;
import org.apache.camel.dataformat.csv.CsvDataFormat;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.apache.camel.Exchange;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;

public class FileTransferRoute extends RouteBuilder {

    private static final Logger LOG = LoggerFactory.getLogger(FileTransferRoute.class);

    public static void main(String[] args) throws Exception {
        Main main = new Main();
        main.configure().addRoutesBuilder(new FileTransferRoute());
        main.run();
    }

    @Override
    public void configure() {
        // CSV -> JSON using CsvDataFormat and Jackson
        final CsvDataFormat csv = new CsvDataFormat()
                .setUseMaps(true)
                .setSkipHeaderRecord(true)
                .setHeader("id_envio,cliente,direccion,estado");

        from("file:../input?fileName=envios.csv&noop=true&idempotent=true")
            .routeId("csv-to-json-envios")
            .log("[INFO] Procesando archivo: ${file:name}")
            .unmarshal(csv)
            .process(exchange -> {
                @SuppressWarnings("unchecked")
                List<Map<String, Object>> rows = exchange.getIn().getBody(List.class);
                int count = rows != null ? rows.size() : 0;
                LOG.info("[INFO] Archivo cargado con {} registros.", count);
            })
            .marshal().json(JsonLibrary.Jackson)
            .process(exchange -> LOG.info("[INFO] Datos transformados a formato JSON."))
            .to("file:../output?fileName=envios.json")
            .log("[INFO] JSON generado en output/envios.json");
    }
}
