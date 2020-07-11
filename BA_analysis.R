#Steven A Vasquez
#Date Created 12/2/2019
#Last modified 12/3/2019
#Used to created animated graph

setwd('~/linux')

#Load Modules needed
library(tidyverse)
library(lubridate)
library(gganimate)

#Load in data

indego_trips <- read_csv('indego-trips-2019-q3.csv')
clean_indego <- na.omit(indego_trips)

#Make sure dates are recognized as dates
#parse_date(indego_trips$start_time, 'mdy hh:mm')
#parse_time(indego_trips$start_time, "7/1/2019 0:01")

#Explore data
glimpse(clean_indego)

#parse Dates
clean_indego$start_time <- as.Date(clean_indego$start_time)
clean_indego$end_time <- as.Date(clean_indego$end_time)
clean_indego$values <- 0

#Group by Date
  
Standard <- clean_indego %>% select(bike_type) %>% filter(bike_type=='standard')




clean_indego %>% ggplot(aes(x=bike_type, fill = bike_type))+
  geom_bar()+
  labs(title = 'Day ; {frame time}',x = 'Bike Type',y='Count')+
  theme_classic()+
  transition_time(month)

transition_states(transition_length = 2, 
                    state_length = 1 )+
  ease_aes('sine-in-out')

