###scale_y_continuous(limits=c(-10000, 35000),breaks=seq(-10000,35000,10000))
###scale_y_continuous(limits=c(-40000, 140000),breaks=seq(-40000,140000,40000))
install.packages('ggplot2')
library(ggplot2)
dat1 <- read.csv('D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/data/ChangesAllocation_option_01.csv', header = T)
dat2 <- read.csv('D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/data/ChangesAllocation_option_02.csv', header = T)
dat3 <- read.csv('D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/data/ChangesAllocation_option_03.csv', header = T)
dat4 <- read.csv('D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/data/ChangesAllocation_option_04_final.csv', header = T)




theme_zg <- function(..., bg='transparent'){
    require(grid)
    theme_classic(...) +
        theme(rect=element_rect(fill=bg),  
              strip.background = element_rect(fill="#dddddd", color='transparent', linetype = NULL,),
              #panel.background=element_rect(fill='transparent', color='black', size=1),
              panel.border=element_rect(fill='transparent', color='black', size=1),
              panel.grid=element_blank(),

              axis.title = element_text(color='black', vjust=0.1),
              axis.ticks.length = unit(0.5,"lines"),
              axis.ticks = element_line(color='black'),
              #axis.ticks.margin = unit(1,"lines"),
              legend.title=element_blank(),
              legend.key=element_rect(fill='transparent', color='transparent'))
}


q <- ggplot(dat1, mapping=aes(x=year, y=BUChange, fill=By)) +
     scale_y_continuous(limits=c(-10000, 35000),breaks=seq(-10000,35000,10000))+
     geom_bar(stat ="identity",width = 0.5,position =position_dodge(),alpha=0.7) +
     scale_fill_manual(name='--',
                     values=c('#ca0020','#0571b0'))+
     geom_hline(aes(yintercept=0)) 

q1 <- q + facet_wrap(nrow=3, ncol=4, ~world_region) +
  theme_zg()

ggsave("D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/figure/option 01.pdf", q1, width = 10.7, height = 7.4, dpi = 300)
  


w <- ggplot(dat2, mapping=aes(x=year, y=BUChange, fill=By)) +
     scale_y_continuous(limits=c(-10000, 35000),breaks=seq(-10000,35000,10000)) +
     geom_bar(stat ="identity",width = 0.5,position =position_dodge(),alpha=0.7) +
     scale_fill_manual(name='--',
                     values=c('#ca0020','#0571b0'))+
     geom_hline(aes(yintercept=0)) 

w1 <- w + facet_wrap(nrow=3, ncol=4, ~world_region) +
  theme_zg()

ggsave("D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/figure/option 02.pdf", w1, width = 10.7, height = 7.4, dpi = 300)

x <- ggplot(dat3, mapping=aes(x=year, y=BUChange, fill=By)) +
     scale_y_continuous(limits=c(-10000, 35000),breaks=seq(-10000,35000,10000)) +
     geom_bar(stat ="identity",width = 0.5,position =position_dodge(),alpha=0.7) +
     scale_fill_manual(name='--',
                     values=c('#ca0020','#0571b0'))+
     geom_hline(aes(yintercept=0)) 

x1 <- x + facet_wrap(nrow=3, ncol=4, ~world_region) +
  theme_zg()

ggsave("D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/figure/option 03.pdf", x1, width = 10.7, height = 7.4, dpi = 300)


y <- ggplot(dat4, mapping=aes(x=year, y=BUChange, fill=By)) +
     scale_y_continuous(limits=c(-10000, 35000),breaks=seq(-10000,35000,10000)) +
     geom_bar(stat ="identity",width = 0.5,position =position_dodge(),alpha=0.7) +
     scale_fill_manual(name='--',
                     values=c('#ca0020','#0571b0'))+
     geom_hline(aes(yintercept=0)) 

y1 <- y + facet_wrap(nrow=3, ncol=4, ~world_region) +
  theme_zg()

ggsave("D:/SURFdrive/UrbanDensity/manuscript/LANDUP-RV2/manuscript_20210818/figure/option 04.pdf", y1, width = 10.7, height = 7.4, dpi = 300)




