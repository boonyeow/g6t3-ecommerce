package com.esd.review;

import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
public class ReviewService {
    private final ReviewRepository reviewRepository;

    @Autowired
    public ReviewService(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
    }

    public ResponseEntity<?> getReviewsByProductId(int productId) {
        try {
            List<Review> reviewsByProductId = reviewRepository.getReviewsByProductId(productId);
            return ResponseEntity.status(HttpStatus.OK).body(reviewsByProductId);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage().equals("") ? "Unable to get reviews." : e.getMessage());
        }
    }

    public ResponseEntity<?> getReviewsByUserId(int userId) {
        try {
            List<Review> reviewsByUserId = reviewRepository.getReviewsByUserId(userId);
            return ResponseEntity.status(HttpStatus.OK).body(reviewsByUserId);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage().equals("") ? "Unable to get reviews." : e.getMessage());
        }
    }

    public ResponseEntity<?> createReview(Review review) {
        try {
            review.setId(ObjectId.get().toString());
            review.setReviewDate(new Date());
            checkDuplicateReview(review.getProductId(), review.getUserId());
            Review savedReview = reviewRepository.save(review);
            return ResponseEntity.status(HttpStatus.CREATED).body(savedReview);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.METHOD_NOT_ALLOWED).body(e.getMessage().equals("") ? "Unable to create review." : e.getMessage());
        }
    }

    public ResponseEntity<?> deleteReviewByReviewId(String reviewId) {
        reviewRepository.deleteById(reviewId);
        return ResponseEntity.status(HttpStatus.OK).body("Successfully deleted!");
    }

    private void checkDuplicateReview(int productId, int userId) throws Exception {
        boolean duplicate = reviewRepository.existsByProductIdAndUserId(productId, userId);
        if (duplicate) {
            throw new Exception("Review from this user on the product already exists.");
        }
    }

}
