package com.esd.review;

import com.esd.response.Response;
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

    public ResponseEntity<Response> getReviewsByProductId(String product_id) {
        try {
            List<Review> reviewsByProductId = reviewRepository.getReviewsByProductId(product_id);
            return ResponseEntity.status(HttpStatus.OK).body(new Response(HttpStatus.OK.value(), reviewsByProductId, "Success!"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new Response(HttpStatus.INTERNAL_SERVER_ERROR.value(), null, e.getMessage().equals("") ? "Unable to get reviews." : e.getMessage()));
        }
    }

    public ResponseEntity<Response> getReviewsByUserId(String userId) {
        try {
            List<Review> reviewsByUserId = reviewRepository.getReviewsByUserId(userId);
            return ResponseEntity.status(HttpStatus.OK).body(new Response(HttpStatus.OK.value(), reviewsByUserId, "Success!"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new Response(HttpStatus.INTERNAL_SERVER_ERROR.value(), null, e.getMessage().equals("") ? "Unable to get reviews." : e.getMessage()));
        }
    }

    public ResponseEntity<Response> createReview(Review review) {
        try {
            review.setId(ObjectId.get().toString());
            review.setReview_date(new Date());
            checkDuplicateReview(review.getProduct_id(), review.getUser_id());
            Review savedReview = reviewRepository.save(review);
            return ResponseEntity.status(HttpStatus.CREATED).body(new Response(HttpStatus.OK.value(), savedReview, "Success!"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.METHOD_NOT_ALLOWED).body(new Response(HttpStatus.INTERNAL_SERVER_ERROR.value(), null, e.getMessage().equals("") ? "Unable to create review." : e.getMessage()));
        }
    }

    public ResponseEntity<Response> deleteReviewByReviewId(String reviewId) {
        reviewRepository.deleteById(reviewId);
        return ResponseEntity.status(HttpStatus.OK).body(new Response(HttpStatus.OK.value(), null, "Success!"));
    }

    private void checkDuplicateReview(String productId, String userId) throws Exception {
        boolean duplicate = reviewRepository.existsByProductIdAndUserId(productId, userId);
        if (duplicate) {
            throw new Exception("Review from this user on the product already exists.");
        }
    }

}
