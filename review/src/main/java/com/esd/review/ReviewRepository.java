package com.esd.review;

import org.springframework.data.mongodb.repository.ExistsQuery;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.util.List;

public interface ReviewRepository extends MongoRepository<Review, String> {
    @ExistsQuery("{'product_id': ?0, 'user_id': ?1}")
    boolean existsByProductIdAndUserId(int productId, int userId);

    @Query("{'product_id': ?0}")
    List<Review> getReviewsByProductId(int productId);

    @Query("{'user_id': ?0}")
    List<Review> getReviewsByUserId(int userId);
}
