package com.esd.review;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.Date;

@Document(collection = "review_details")
public class Review {
    @Id
    private String id;
    @Field("product_id")
    private int productId;
    @Field("user_id")
    private int userId;
    @Field("review_description")
    private String reviewDescription;
    @Field("review_date")
    private Date reviewDate;

    public Review(String id, int productId, int userId, String reviewDescription, Date reviewDate) {
        this.id = id;
        this.productId = productId;
        this.userId = userId;
        this.reviewDescription = reviewDescription;
        this.reviewDate = reviewDate;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getProductId() {
        return productId;
    }

    public void setProductId(int productId) {
        this.productId = productId;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getReviewDescription() {
        return reviewDescription;
    }

    public void setReviewDescription(String reviewDescription) {
        this.reviewDescription = reviewDescription;
    }

    public Date getReviewDate() {
        return reviewDate;
    }

    public void setReviewDate(Date reviewDate) {
        this.reviewDate = reviewDate;
    }
}
