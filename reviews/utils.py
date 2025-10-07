def calculate_average_rating(reviews_queryset):
    """
    Calculate the average rating from a QuerySet of reviews.

    Args:
        reviews_queryset (QuerySet): Django QuerySet of review objects having a 'rating' field.

    Returns:
        float: Average rating (0.0 if no reviews).
    """
    try:
        # Handle empty queryset
        if not reviews_queryset.exists():
            return 0.0

        total_rating = 0
        count = reviews_queryset.count()

        for review in reviews_queryset:
            total_rating += review.rating

        average = total_rating / count
        return round(average, 2)  # rounded to 2 decimal places for readability

    except Exception as e:
        # Log or print error if needed
        print(f"Error calculating average rating: {e}")
        return 0.0
