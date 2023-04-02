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

    @GetMapping("/get/product/{product_id}")
    public ResponseEntity<?> getReviewByProductId(@PathVariable String product_id) {
        return reviewService.getReviewsByProductId(product_id);
    }

    @GetMapping("/get/user/{userId}")
    public ResponseEntity<?> getReviewsByUserId(@PathVariable String user_id) {
        return reviewService.getReviewsByUserId(user_id);
    }

    @PostMapping
    public ResponseEntity<?> createReview(@RequestBody Review review) {
        return reviewService.createReview(review);
    }

    @DeleteMapping("/{review_id}")
    public ResponseEntity<?> deleteReview(@PathVariable String review_id) {
        return reviewService.deleteReviewByReviewId(review_id);
    }
}
