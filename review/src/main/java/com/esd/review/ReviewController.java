package com.esd.review;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(path = "/review")
public class ReviewController {
    private final ReviewService reviewService;

    @Autowired
    public ReviewController(ReviewService reviewService) {
        this.reviewService = reviewService;
    }

    @GetMapping("/get/product/{productId}")
    public ResponseEntity<?> getReviewByProductId(@PathVariable int productId) {
        return reviewService.getReviewsByProductId(productId);
    }

    @GetMapping("/get/user/{userId}")
    public ResponseEntity<?> getReviewsByUserId(@PathVariable int userId) {
        return reviewService.getReviewsByUserId(userId);
    }


    @PostMapping
    public ResponseEntity<?> createReview(@RequestBody Review review) {
        return reviewService.createReview(review);
    }

    @DeleteMapping("/{reviewId}")
    public ResponseEntity<?> deleteReview(@PathVariable String reviewId) {
        return reviewService.deleteReviewByReviewId(reviewId);
    }
}
