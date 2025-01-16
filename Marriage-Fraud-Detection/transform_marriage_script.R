library(tidyverse)
library(dplyr)


df <- read.csv('C:/Users/Khanh/Desktop/GMUeducation/DAEN_690/DATA/synthetic-data-1-1mil.csv')
names(df)


df$Income <- df$Annual.Income..I.864.
df$NumChildren <- df$Children.Count..I.130.
df$NumDivorce <- df$Number.of.Previous.Marriages..I.130.
max(df$NumDivorce)

df$Age <- as.numeric(df$Age)
df$Spouse...Age..I.130. <- as.numeric(df$Spouse...Age..I.130.)

max(df$Age)
min(df$Age)
min(df$Spouse...Age..I.130.)
max(df$Spouse...Age..I.130.)
spouse_age <- sort(df$Spouse...Age..I.130.)
tail(sort(spouse_age), 20)
df$Spouse...Age..I.130. <- replace(df$Spouse...Age..I.130., df$Spouse...Age..I.130.>90, 90)

df <- df %>% mutate(Age_Gap = abs(Age - Spouse...Age..I.130.))
max(df$Age_Gap)

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

#write.csv(transformed_df1, "C:/Users/Khanh/Desktop/GMUeducation/DAEN_690/DATA/transformed_1mil_qvm_data.csv", row.names = FALSE )


####Fraud used aggregation with 2 identifiers

df$FraudAlert <- ifelse(df$BigAgeGap + df$TooLowIncome + df$TooManyChildren + df$TooManyDivorce + 
                          df$CriminalHistory + df$PreviousImmigrationProblem + df$DiffAddress + df$DiffLanguage >=2, 1, 0)
table(df$FraudAlert)

#transformed_df <- df %>% select(Income, Age_Gap, NumChildren, NumDivorce, DiffLanguage, DiffAddress, PreviousImmigrationProblem, CriminalHistory, TooManyChildren, TooLowIncome, TooManyDivorce, BigAgeGap, FraudAlert)

##transformed_df <- select(df$Income, df$Age_Gap, df$NumChildren, df$NumDivorce, df$DiffLanguage, df$DiffAddress, df$PreviousImmigrationProblem, df$CriminalHistory, df$TooManyChildren, df$TooLowIncome, df$TooManyDivorce, df$BigAgeGap, df$FraudAlerted)


transformed_df <- rename(df, c(Balance_of_Saving_and_Checking_accounts = "Balance.of.Savings.and.Checkings.account..I.864.",
                               Current_value_investment_accounts = "Current.cash.value.of.stocks..bonds..etc...I.864.",
                               Annual_Income = "Annual.Income..I.864.",
                               Country_of_birth = "Country.of.Birth..I.130.",
                               First_Petition_for_Beneficiary = "First.Petition.for.Beneficiary..I.130.",
                               Beneficiary_Ever_in_Immigration_Proceedings = "Beneficiary.Ever.in.Immigration.Proceedings..I.130.",
                               Criminal_History = "Criminal.History..N.400.",
                               Spouse_Age = "Spouse...Age..I.130.",
                               Race_Ethnicity = "Race.Ethnicity..I.130.",
                               Spouse_Race_Ethnicity = "Spouse...Race.Ethnicity..I.130.",
                               Religion = "Religion..I.130.",
                               Spouse_Religion = "Spouse...Religion..I.130.",
                               Language = "Language..I.130.",
                               Spouse_Language = "Spouse...Language..I.130.",
                               Children_Count = "Children.Count..I.130.",
                               Address = "Address..I.130.",
                               Spouse_Address = "Spouse...Address..I.130.",
                               Number_of_Previous_Marriages = "Number.of.Previous.Marriages..I.130.",
                               Length_of_Marriage1 = "Length.of.Marriage.1...Years..I.130.",
                               Length_of_Marriage2 = "Length.of.Marriage.2...Years..I.130.",
                               Length_of_Marriage3 = "Length.of.Marriage.3...Years..I.130.",
                               Length_of_Marriage4 = "Length.of.Marriage.4...Years..I.130.",
                               Length_of_Marriage5 = "Length.of.Marriage.5...Years..I.130.",
                               Dating_Length = "Dating.Length..I.130.Interview.",
                               Recent_Joint_Bank_Accounts = "Recent.Joint.Bank.Accounts..I.130.Interview.",
                               Nervousness_at_I130_Interview = "Nervousness.at.I.130.Interview..I.130.Interview.",
                               Known_Fraudulent = "Known.Fradulent"))

#transformed_df$Spouse_Age <- replace(transformed_df$Spouse_Age, transformed_df$Spouse_Age>90, 90)

marriage_dataset <- subset(transformed_df, select = -c(Known_Fraudulent, FraudAlerted))

write.csv(marriage_dataset, "C:/Users/Khanh/Desktop/GMUeducation/ECE552/FinalProject/marriage_dataset.csv", row.names = FALSE )

