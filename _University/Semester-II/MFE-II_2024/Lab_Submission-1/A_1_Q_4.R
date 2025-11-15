total_cards <- 52
black <- 26
red <-26
heart <- 13
diamond <- 13
spade <- 13
club <- 13
queen_d <- 1
king_s <- 1
king_d <- 1
jaques_h <- 1

#With Replacement

# Part a:
probability_a <- (queen_d/total_cards)*(king_s/total_cards)*(king_d/total_cards)*(jaques_h/total_cards)
print("Probability in a part: ")
print(probability_a)

# Part b:
probability_b <-(black/total_cards)**4
print("Probability of all 4 cards are black: ")
print(probability_b)

# Part c:
card_9 <- 1
probability_c <- (card_9/total_cards)*(heart/total_cards)*(heart/total_cards)*(red/total_cards)
print("Probability in c part: ")
print(probability_c)

# Part d:
probability_d <- (heart/total_cards)**4
print("Probability of all 4 cards are hearts: ")
print(probability_d)

# Part e:
card_9 <- 1
probability_e <-((total_cards-card_9)/total_cards)**4
print("Probability that none of the card is a 9: ")
print(probability_e)

#Without Replacement

# Part a:
probability_a_w <- (queen_d/total_cards)*(king_s/(total_cards-1))*(king_d/(total_cards-2))*(jaques_h/(total_cards-3))
print("Probability in a part: ")
print(probability_a_w)

# Part b:
probability_b_w <-(black/total_cards)*((black-1)/(total_cards-1))*((black-2)/(total_cards-2))*((black-3)/(total_cards-3))
print("Probability of all 4 cards are black: ")
print(probability_b_w)

# Part c:
probability_c_w <- (card_9/total_cards)*((heart-1)/total_cards)*((heart-2)/total_cards)*((red-3)/total_cards)
print("Probability in c part: ")
print(probability_c_w)

# Part d:
probability_d_w <-(heart/total_cards)*((heart-1)/(total_cards-1))*((heart-2)/(total_cards-2))*((heart-3)/(total_cards-3))
print("Probability of all 4 cards are hearts: ")

print(probability_d_w)

# Part e:
probability_e_w <-((total_cards-card_9)/total_cards)*((total_cards-card_9-1)/(total_cards-1))*((total_cards-card_9-2)/(total_cards-2))*((total_cards-card_9-3)/(total_cards-3))
print("Probability that none of the card is a 9: ")
print(probability_e_w)

