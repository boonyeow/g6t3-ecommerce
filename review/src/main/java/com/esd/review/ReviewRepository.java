package com.esd.review;

import org.springframework.data.mongodb.repository.ExistsQuery;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.util.List;

public interface ReviewRepository extends MongoRepository<Review, String> {
    @ExistsQuery("{ 'product_id': ?0, 'user_id': ?1, 'order_id': ?2}")
    boolean existsByProductIdAndUserIdAndOrderId(String product_Id, String user_id, String order_id);

    @Query("{'product_id': ?0}")
    List<Review> getReviewsByProductId(String product_id);

    @Query("{'user_id': ?0}")
    List<Review> getReviewsByUserId(String user_id);
}
