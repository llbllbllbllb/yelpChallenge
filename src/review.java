public class review{
    private  String review_id = "";
    private String business_id = "";
    private String user_id = "";
    private String username = "";
    private String businessname = "";
    private int stars = 0;
    private String reviewDate = "";
    private String reviewTime = "";
    private String reviewText = "";
    private int useful = 0;
    private int funny = 0;
    private int cool = 0;

    public review(){}

    public review(String review_id, String business_id, String user_id, String username, String businessname, int stars, String reviewDate, String reviewTime, String reviewText, int useful, int funny, int cool) {
        this.review_id = review_id;
        this.business_id = business_id;
        this.user_id = user_id;
        this.username = username;
        this.businessname = businessname;
        this.stars = stars;
        this.reviewDate = reviewDate;
        this.reviewTime = reviewTime;
        this.reviewText = reviewText;
        this.useful = useful;
        this.funny = funny;
        this.cool = cool;
    }

    public String getReview_id() {
        return review_id;
    }

    public void setReview_id(String review_id) {
        this.review_id = review_id;
    }

    public String getBusiness_id() {
        return business_id;
    }

    public void setBusiness_id(String business_id) {
        this.business_id = business_id;
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getBusinessname() {
        return businessname;
    }

    public void setBusinessname(String businessname) {
        this.businessname = businessname;
    }

    public int getStars() {
        return stars;
    }

    public void setStars(int stars) {
        this.stars = stars;
    }

    public String getReviewDate() {
        return reviewDate;
    }

    public void setReviewDate(String reviewDate) {
        this.reviewDate = reviewDate;
    }

    public String getReviewTime() {
        return reviewTime;
    }

    public void setReviewTime(String reviewTime) {
        this.reviewTime = reviewTime;
    }

    public String getReviewText() {
        return reviewText;
    }

    public void setReviewText(String reviewText) {
        this.reviewText = reviewText;
    }

    public int getUseful() {
        return useful;
    }

    public void setUseful(int useful) {
        this.useful = useful;
    }

    public int getFunny() {
        return funny;
    }

    public void setFunny(int funny) {
        this.funny = funny;
    }

    public int getCool() {
        return cool;
    }

    public void setCool(int cool) {
        this.cool = cool;
    }
}