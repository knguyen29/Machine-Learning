library(tidyverse)
library(dplyr)


df <- read.csv('C:/Users/Khanh/Desktop/GMUeducation/ECE552/FinalProject/synthetic-data-dev.csv')
names(df)


df$Income <- df$Annual.Income..I.864.
df$NumChildren <- df$Children.Count..I.130.
df$NumDivorce <- df$Number.of.Previous.Marriages..I.130.
max(df$NumDivorce)

df$Age <- as.numeric(df$Age)
df$Spouse...Age..I.130. <- as.numeric(df$Spouse...Age..I.130.)
df <- df %>% mutate(Age_Gap = abs(Age - Spouse...Age..I.130.))
max(df$Age_Gap)
max(df$Age)
min(df$Age)
min(df$Spouse...Age..I.130.)
max(df$Spouse...Age..I.130.)
spouse_age <- sort(df$Spouse...Age..I.130.)
tail(sort(spouse_age), 20)

df$Language..I.130. <- as.character(df$Language..I.130.)
df$Spouse...Language..I.130. <- as.character(df$Spouse...Language..I.130.)
df$DiffLanguage <- ifelse(df$Language..I.130. == df$Spouse...Language..I.130., 0, 1)
table(df$DiffLanguage)

df$Address..I.130. <- as.character(df$Address..I.130.)
df$Spouse...Address..I.130. <- as.character(df$Spouse...Address..I.130.)
df$DiffAddress <- ifelse(df$Address..I.130. == df$Spouse...Address..I.130., 0, 1)
table(df$DiffAddress)

df$PreviousImmigrationProblem <- ifelse(df$Beneficiary.Ever.in.Immigration.Proceedings..I.130. == "True", 1, 0)
table(df$PreviousImmigrationProblem)
table(df$Beneficiary.Ever.in.Immigration.Proceedings..I.130.)

df$CriminalHistory <- ifelse(df$Criminal.History..N.400. == "True", 1, 0)
table(df$CriminalHistory)
table(df$Criminal.History..N.400.)

df$TooManyChildren <- ifelse(df$NumChildren >=5, 1, 0)
table(df$TooManyChildren)

df$TooManyDivorce <- ifelse(df$NumDivorce >=3, 1, 0)
table(df$TooManyDivorce)

df$TooLowIncome <- ifelse(df$Income < 15000, 1, 0)
table(df$TooLowIncome)

df$BigAgeGap <- ifelse(df$Age_Gap > 15, 1, 0)
table(df$BigAgeGap)

df$FraudAlerted <- df$Known.Fradulent
transformed_df1 <- df %>% select(Income, Age_Gap, NumChildren, NumDivorce, DiffLanguage, DiffAddress, PreviousImmigrationProblem, CriminalHistory, TooManyChildren, TooLowIncome, TooManyDivorce, BigAgeGap, FraudAlerted)
table(df$FraudAlerted)

write.csv(transformed_df1, "C:/Users/Khanh/Desktop/GMUeducation/ECE552/FinalProject/transformed_data.csv", row.names = FALSE )


####Fraud used aggregation with 2 identifiers

df$FraudAlert <- ifelse(df$BigAgeGap + df$TooLowIncome + df$TooManyChildren + df$TooManyDivorce + 
                              df$CriminalHistory + df$PreviousImmigrationProblem + df$DiffAddress + df$DiffLanguage >=2, 1, 0)
table(df$FraudAlert)

transformed_df <- df %>% select(Income, Age_Gap, NumChildren, NumDivorce, DiffLanguage, DiffAddress, PreviousImmigrationProblem, CriminalHistory, TooManyChildren, TooLowIncome, TooManyDivorce, BigAgeGap, FraudAlert)

#transformed_df <- select(df$Income, df$Age_Gap, df$NumChildren, df$NumDivorce, df$DiffLanguage, df$DiffAddress, df$PreviousImmigrationProblem, df$CriminalHistory, df$TooManyChildren, df$TooLowIncome, df$TooManyDivorce, df$BigAgeGap, df$FraudAlerted)

write.csv(transformed_df, ".../transformed_dataset.csv", row.names = FALSE )

