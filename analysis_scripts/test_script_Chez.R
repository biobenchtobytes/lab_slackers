my_data = read.csv('raw_data.csv', header=TRUE, sep=",")
head(my_data)
library(ggplot2)
my_data = my_data[1:3]
my_data
colnames(my_data) = c('A','B','C')
my_plot = ggplot(my_data, aes(x = Daily.active.members, y = Messages.in.DMs)) + geom_point()
my_plot
ggsave('Chez_plot.png')

