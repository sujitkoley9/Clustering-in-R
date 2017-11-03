#-----------------------------Step 1:Importing Library-------------------------------------------

  library(ggplot2)
  library(ggdendro)

#-----------------------------Step 2:Read CSV file-----------------------------------------------

  setwd("W:\\R code\\Clustering")
  FootballPlayerRecords <- read.csv("Song_Football.csv")
  View(FootballPlayerRecords)

#----------------------------Step 3: Preparing Data quality Report-------------------------------
  str(FootballPlayerRecords)
  summary(FootballPlayerRecords)
  
  DataTypes <-1
  Maxs<-1
  Mins<-1
  Average<-1
  SD<-1
  U<-1
  
  variable<-names(FootballPlayerRecords)
  
  for(i in 1:length(variable))
  {
    x<-variable[i]
    y<-FootballPlayerRecords[,x] #all the values present in a given column
    
    DataTypes[i] <-class(y)
    Maxs[i]<-ifelse((class(y)=="integer" | class(y)=="numeric"),max(y,na.rm=TRUE),0)
    Mins[i]<-ifelse((class(y)=="integer" | class(y)=="numeric"),min(y,na.rm=TRUE),0)
    Average[i]<-as.integer(ifelse((class(y)=="integer" | class(y)=="numeric"),mean(y,na.rm=TRUE),0))
    SD[i]<-ifelse((class(y)=="integer" | class(y)=="numeric"),sd(y,na.rm=TRUE),0)
    U[i]<-ifelse(class(y)=="factor" ,unique(y),0)
    
  }
  
  missing_count<-colSums(is.na(FootballPlayerRecords))
  
  final_summary<-data.frame(variable=names(FootballPlayerRecords),data_type=DataTypes,Min=Mins,Max=Maxs,
                            average=Average,SD=SD,unique=U,missing=missing_count)
  
  
  rownames(final_summary) <- NULL
  write.csv(final_summary,file="Data_report.csv")
  
  
#----------------------------Step 4: Missing value treatment--------------------------------------
   # There is no missing, no actions required

#----------------------------Step 5: outlier  treatment--------------------------------------
    # outliers doesn't affect clustering there is no need to remove or impute the oulier
    # If there are outlier they will automatically assign to a single cluster
  
#----------------------------Step 6: Check information about insured player Song -----------------
  
song <- FootballPlayerRecords[which(FootballPlayerRecords$First_Name=='Song'),] 
View(song)


#----------------------------Step 7: Data preparation for clutering------------------------------

  # keeping only the numeric values
  # for clustering we don't need 1st column and use col 2:8
FootballPlayerRecords_Clustering <- FootballPlayerRecords[,2:8]

# scaling ( ordering is same)
FootballPlayerRecords_Clustering <- scale(FootballPlayerRecords_Clustering,
                                          center=TRUE,scale=TRUE)

# weighting tackles by 3
FootballPlayerRecords_Clustering[,1] <- FootballPlayerRecords_Clustering[,1]*3


#------------------------Step 8: find the optimal number of clusters( K value) using elbow method----

#Create a screeplot-plot of cluster's tot.withinss wrt number of clusters

  wss<-1:15
  number<-1:15
  
  for (i in 1:15)
    
  {
    wss[i]<-kmeans(FootballPlayerRecords_Clustering,i)$tot.withinss
  }

  
  data<-data.frame(wss,number)
  p<-ggplot(data,aes(x=number,y=wss),color="red")
  p+geom_point()
 # According to Scatterplot , optimal k value =8

#------------------------Step 9: Building cluster and assigning to players records --------------
 
  set.seed(8)
  Clusters_result <- kmeans(FootballPlayerRecords_Clustering ,8)  
  
  FootballPlayerRecords$Cluster_no <- Clusters_result$cluster
  
#------------------------Step 10: Finding players similar to Song -------------------------------
  
  Song_cluster <- FootballPlayerRecords[which(FootballPlayerRecords$First_Name=='Song'),]
  
  Players_similar_to_song <-FootballPlayerRecords[which(FootballPlayerRecords$Cluster_no==
                                                          Song_cluster$Cluster_no),] 
  
  View(Players_similar_to_song)
  

  
#------------------------------Different Approch:Using Hierarchical cluster -------------------
  
  d <- dist(FootballPlayerRecords_Clustering, method = "euclidean")
  
  HCluster_result <- hclust(d,method ="average" )
  plot(HCluster_result,
       main = 'Dendrogram',
       xlab = 'Player',
       ylab = 'Euclidean distances') # display dendogram
  
  ggdendrogram(HCluster_result, 
               rotate = FALSE, 
               theme_dendro = TRUE, 
               color = "tomato")
  
  
  hc_fit = cutree(HCluster_result, 7)
  
  FootballPlayerRecords$Cluster_no <- hc_fit
  
  
  Song_cluster <- FootballPlayerRecords[which(FootballPlayerRecords$First_Name=='Song'),]
  
  Players_similar_to_song <-FootballPlayerRecords[which(FootballPlayerRecords$Cluster_no==
                                                          Song_cluster$Cluster_no),] 
  
  View(Players_similar_to_song)
  
  
  