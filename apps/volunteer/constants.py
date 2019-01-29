GENDER_CHOICES = [
    ('m', 'Male'),
    ('f', 'Female')
]
WEEKDAY_CHOICES = [
    (5, 'Saturday'),
    (6, 'Sunday'),
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
]
SLOT_TIME_CHOICES = [
    (0, 'Morning'),
    (1, 'Noon'),
    (2, 'Afternoon'),
    (3, 'Night'),
]

REQUEST_STATUS_CHOICES = [
    (0, 'PENDING'),
    (-1, 'REJECTED'),
    (1, 'ACCEPTED')
]

REQUEST_TARGET_CHOICES = [
    (0, 'CHARITY'),
    (1, 'VOLUNTEER')
]

RATING_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]
