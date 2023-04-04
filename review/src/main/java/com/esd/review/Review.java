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
    private String product_id;
    @Field("user_id")
    private String user_id;
    @Field("order_id")
    private String order_id;
    @Field("review_description")
    private String review_description;
    @Field("review_stars")
    private int review_stars;
    @Field("review_date")
    private Date review_date;
    @Field("purchase_date")
    private Date purchase_date;

    public Review(String id, String product_id, String user_id, String order_id, String review_description, int review_stars, Date review_date, Date purchase_date) {
        this.id = id;
        this.product_id = product_id;
        this.user_id = user_id;
        this.order_id = order_id;
        this.review_description = review_description;
        this.review_stars = review_stars;
        this.review_date = review_date;
        this.purchase_date = purchase_date;
    }

    public String getOrder_id() {
        return order_id;
    }

    public void setOrder_id(String order_id) {
        this.order_id = order_id;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getProduct_id() {
        return product_id;
    }

    public void setProduct_id(String product_id) {
        this.product_id = product_id;
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public String getReview_description() {
        return review_description;
    }

    public void setReview_description(String review_description) {
        this.review_description = review_description;
    }

    public int getReview_stars() {
        return review_stars;
    }

    public void setReview_stars(int review_stars) {
        this.review_stars = review_stars;
    }

    public Date getReview_date() {
        return review_date;
    }

    public void setReview_date(Date review_date) {
        this.review_date = review_date;
    }

    public Date getPurchase_date() {
        return purchase_date;
    }

    public void setPurchase_date(Date purchase_date) {
        this.purchase_date = purchase_date;
    }
}
