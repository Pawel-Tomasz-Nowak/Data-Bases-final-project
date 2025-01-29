SELECT 
    EXTRACT(YEAR FROM T.data_transakcji) AS Rok,
    EXTRACT(MONTH FROM T.data_transakcji) AS Miesiac,
    COUNT(DISTINCT T.id_klienta) AS Liczba_Studentów
FROM 
    Transakcje T
JOIN 
    Klienci K ON T.id_klienta = K.id_klienta
WHERE 
    ROUND(K.znizka, 2) = 0.49 
GROUP BY 
    EXTRACT(YEAR FROM T.data_transakcji), EXTRACT(MONTH FROM T.data_transakcji)
ORDER BY 
    Rok, Miesiac;
