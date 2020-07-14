#Steven A Vasquez


#Upload Needed packages
library(Lahman)
library(GGally)
library(tidyverse)
library(corrplot)

#View structure of wanted Data frame
str(Teams)
glimpse(Teams)
head(Teams)
tail(Teams)

#Separate Teams to separate variable, only include teams from year 2001 till now
#Add Basic sabermetrics to Data Frame 
team_wins_ <- Teams %>% select(-(franchID:Ghome),-(DivWin:WSWin), -(ER:teamIDretro)) %>% filter(yearID>2000,) %>% 
  mutate(wpct = R^2/(R^2+RA^2),expwin = round(wpct*(W+L)),Rdiff = W-expwin,
         PA = AB + HBP + BB  + SF,
         X1B = H - X2B - X3B - HR,
         TB = X1B + 2*X2B + 3*X3B + 4*HR,
         BA = round(H/AB,3),
         OBP = round((H + BB + HBP)/(PA),3),
         SLG = round(TB/AB,3),
         OPS = OBP + SLG,
         ISO = round((X2B + 2*X3B + 3*HR)/AB,3),
         RC = round((H + BB - CS)* (TB + .55*SB)/(AB + BB)),
         BRA = round(OBP * SLG,3),
         SOR = round(SO/PA,3),
         BBR = round(BB/PA,3))

#Create new variable for each year 
# Create & Save Correlation Matrix for each year being evaluated 
team_2001<- team_wins_ %>% filter(yearID==2001) %>% select(R, BA, OBP, SLG,OPS,ISO,RC,BRA,SOR,BBR) 
png("Team 2001")
cor(team_2001) %>% corrplot.mixed()
dev.off()
png("2004 Matrix")
team_2004<- team_wins_ %>% filter(yearID==2004) %>% select(R, BA, OBP, SLG,OPS,ISO,RC,BRA,SOR,BBR)
cor(team_2004)%>% corrplot.mixed()
dev.off()
png("2007 Matrix")
team_2007<- team_wins_ %>% filter(yearID==2007) %>% select(R, BA, OBP, SLG,OPS,ISO,RC,BRA,SOR,BBR) 
cor(team_2007)%>% corrplot.mixed()
dev.off()
png("2010 Matrix")
team_2010<- team_wins_ %>% filter(yearID==2010) %>% select(R, BA, OBP, SLG,OPS,ISO,RC,BRA,SOR,BBR)
cor(team_2010)%>% corrplot.mixed()
dev.off()
png("2013 Matrix")
team_2013<- team_wins_ %>% filter(yearID==2013) %>% select(R, BA, OBP, SLG,OPS,ISO,RC,BRA,SOR,BBR) 
cor(team_2013)%>% corrplot.mixed()
dev.off()
png("2016 Matrix")
team_2016<- team_wins_ %>% filter(yearID==2016) %>% select(R, BA, OBP, SLG,OPS,ISO,RC,BRA,SOR,BBR)
cor(team_2016) %>% corrplot.mixed()
dev.off()

#Create and view summary of linear regression done on SLG/BA for each yearw
mod_2001 <- lm(R~ BA , data = team_2001 )
mod_2001_pt2 <- lm(R~ SLG, data = team_2001)
summary(mod_2001)
summary(mod_2001_pt2)
  mod_2004 <- lm(R~ BA + SLG, data = team_2004 )
summary(mod_2004)
mod_2007 <- lm(R~ BA + SLG, data = team_2007 )
summary(mod_2007)
mod_2010 <- lm(R~ BA + SLG, data = team_2010 )
summary(mod_2010)
mod_2013 <- lm(R~ BA + SLG, data = team_2013 )
summary(mod_2013)
mod_2016 <- lm(R~ BA + SLG, data = team_2016 )

#Create visualization of regressions & save graph
png("Linear graph")
ggplot(team_2004,aes(SLG,R))+
  geom_point()+
  ggtitle("Linear Regression SLG")+
  theme_bw()+
  stat_smooth(method = 'lm')
dev.off()

png("Linnear Regression BA")
ggplot(team_2004,aes(BA,R))+
  geom_point()+
  ggtitle("Linear Regression BA")+
  theme_bw()+
  stat_smooth(method = 'lm')
dev.off()

