```

Table players {
  player_id int [pk, increment]
  first_name varchar(100)
  last_name varchar(100)
  date_of_birth date
  country varchar(100)
  position varchar(50)
}

Table clubs {
  club_id int [pk, increment]
  club_name varchar(255) [unique, not null]
}

