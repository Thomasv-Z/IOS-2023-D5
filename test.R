data <- read.csv('OIS.survey.csv')

# verwijder onnodige gegevens
columns_to_remove <- c("Mogen.we.uw.gegevens.anoniem.gebruiken.voor.ons.onderzoek.", "Upload.uw.resultaten.hier", "Knowledge.vanGogh")
data <- data[, !names(data) %in% columns_to_remove]


summary(data)
# Timestamp            Gender          Studie.Program          Age         Knowledge.Dalí  Knowledge.vanGogh Knowledge.Rembrandt
# Length:51          Length:51          Length:51          Min.   :19.00   Min.   :1.000   Min.   :1.000     Min.   :2.000      
# Class :character   Class :character   Class :character   1st Qu.:19.00   1st Qu.:2.000   1st Qu.:3.000     1st Qu.:3.000      
# Mode  :character   Mode  :character   Mode  :character   Median :20.00   Median :3.000   Median :4.000     Median :4.000      
#                                                          Mean   :20.12   Mean   :3.098   Mean   :3.882     Mean   :4.157      
#                                                          3rd Qu.:20.00   3rd Qu.:4.000   3rd Qu.:5.000     3rd Qu.:5.000      
#                                                          Max.   :24.00   Max.   :7.000   Max.   :7.000     Max.   :7.000      
# 
# Experience.LLM  Experience.text.to.image
# Min.   :2.000   Min.   :1.0               
# 1st Qu.:5.000   1st Qu.:2.0         
# Median :6.000   Median :3.0         
# Mean   :5.431   Mean   :3.5                                       
# 3rd Qu.:6.000   3rd Qu.:5.0                                       
# Max.   :7.000   Max.   :7.0                                       
#                 NA's   :1

# Staafdiagram van leeftijden
barplot(table(data$Age), main = "Distribution of Ages in the Dataset", xlab = "Leeftijd", ylab = "Aantal mensen", col = "skyblue")

# Load ggplot2
library(ggplot2)

# Age and Gender
ggplot(data, aes(x = as.factor(Age), fill = Gender)) +
  geom_bar(position = 'stack', color = 'black', size = 0.5) +
  geom_text(stat = 'count', aes(label = ..count..), position = position_stack(vjust = 0.5)) +
  labs(x = 'Age', y = 'Count', title = 'Stacked Bar Plot of Count by Age and Gender') +
  scale_fill_manual(values = c('Man' = 'skyblue', 'Vrouw' = 'pink')) +
  theme_minimal()


# Real vs AI
ggplot(art_data_long, aes(x = paste(Artist, Method), y = Score, fill = Method)) +
  geom_bar(stat = 'identity', position = 'dodge', color = 'black', width = 0.7) +
  geom_text(aes(label = Score), position = position_dodge(width = 0.7), vjust = -0.5) +
  labs(x = '', y = 'Score', title = 'Comparison of Real vs. Ai Scores for Dali and Rembrandt') +
  scale_fill_manual(values = c('Real' = 'skyblue', 'Ai' = 'cyan4'), name = 'Method') +
  theme_minimal()


# AI Choice
ggplot(ai_choice_data_long, aes(x = Images, y = Count, fill = Artist)) +
  geom_bar(stat = 'identity', position = 'dodge', color = 'black', width = 0.7) +
  geom_text(aes(label = Count), position = position_dodge(width = 0.7), vjust = -0.5) +
  labs(x = '', y = 'Count', title = 'AI Choice Comparison for Dali and Rembrandt') +
  scale_fill_manual(values = c('Dali' = 'skyblue', 'Rembrandt' = 'cyan4'), name = 'Artist') +
  theme_minimal()


# Knowledge Dali
ggplot(data, aes(x = "Dali", y = Knowledge.Dali, fill = Studie.Program, group = Studie.Program)) +
  geom_boxplot() +
  labs(x = NULL, y = "Knowledge Level", title = "Comparison of Knowledge Levels (Dali) by Study Program") +
  theme_minimal() +
  theme(legend.position = "right")


# Knowledge Rembrand
ggplot(data, aes(x = "Rembrandt", y = Knowledge.Rembrandt, fill = Studie.Program, group = Studie.Program)) +
  geom_boxplot() +
  labs(x = NULL, y = "Knowledge Level", title = "Comparison of Knowledge Levels (Rembrandt) by Study Program") +
  theme_minimal() +
  theme(legend.position = "right")
