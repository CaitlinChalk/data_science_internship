#script to read and wrangle open data regarding nature spots in the UK 
library(tidyverse)
library(sf)
library(openxlsx)
library(tmap)
library(RColorBrewer)


#we import four different data sets, all from gov.co.uk:
#-----------------------------------------------------------------------

### areas of outstanding natural beauty
#https://naturalengland-defra.opendata.arcgis.com/datasets/areas-of-outstanding-natural-beauty-england/data

nat_beauty.sf <- st_read(dsn = "data/Areas_of_Outstanding_Natural_Beauty_(England)",
layer = "Areas_of_Outstanding_Natural_Beauty__England____Natural_England")

#select columns of interest
nat_beauty.sf <- select(nat_beauty.sf,NAME,geometry)
#rename for consistency with other scripts
nat_beauty.sf <- rename(nat_beauty.sf,name = NAME)
#set crs to 4236
nat_beauty.sf <- st_transform(nat_beauty.sf, 4326)

#National Parks in England
#https://environment.data.gov.uk/DefraDataDownload/?mapService=NE/NationalParksEngland&Mode=spatial
nat_parks.sf <- st_read("data/NE_NationalParksEngland_SHP_Full/data/National_Parks_England.shp")

#select columns of interest
nat_parks.sf <- select(nat_parks.sf,name,geometry)

#set crs to 4236
nat_parks.sf <- st_transform(nat_parks.sf, 4326)

### National nature reserves
#https://environment.data.gov.uk/DefraDataDownload/?mapService=NE/NationalNatureReservesEngland&Mode=spatial
nat_reserves.sf <- st_read("data/NE_NationalNatureReservesEngland_SHP_Full/data/National_Nature_Reserves_England.shp")

#select columns of interest
nat_reserves.sf <- select(nat_reserves.sf,nnr_name,latitude,longitude,geometry)

#rename for consistency
nat_reserves.sf <- rename(nat_reserves.sf,name = nnr_name,lat = latitude,lon = longitude)

#transfrom crs
nat_reserves.sf<- st_transform(nat_reserves.sf, 4326)

#Local nature reserves
#https://environment.data.gov.uk/DefraDataDownload/?mapService=NE/LocalNatureReservesEngland&Mode=spatial
nat_reserves_local.sf <- st_read("data/NE_LocalNatureReservesEngland_SHP_Full/data/Local_Nature_Reserves_England.shp")


#select columns of interest
nat_reserves_local.sf <- select(nat_reserves_local.sf,lnr_name,latitude,longitude,geometry)

#rename for consistency
nat_reserves_local.sf <- rename(nat_reserves_local.sf,name = lnr_name,lat = latitude,lon = longitude)

#transfrom crs
nat_reserves_local.sf <- st_transform(nat_reserves_local.sf, 4326)

#add labels and colours for plotting
nat_beauty.sf$type <- "Areas of outstanding natural beauty"
nat_beauty.sf$colour <- "#238B45"
  
nat_parks.sf$type <- "National parks"
nat_parks.sf$colour <- "#00441B"

nat_reserves.sf$type <- "National nature reserves"
nat_reserves.sf$colour <- "#74C476"

nat_reserves_local.sf$type <- "Local nature reserves"
nat_reserves_local.sf$colour <- "#C7E9C0"

#plot for inspection

#green palette
#brewer.pal(9,"Greens") <- "#F7FCF5" "#E5F5E0" "#C7E9C0" "#A1D99B" "#74C476" "#41AB5D" "#238B45" "#006D2C" "#00441B"
#display.brewer.pal(9,"Greens")

tm_shape(nat_beauty.sf) +
  tm_fill(col = "colour", title = "Areas of outstanding natural beauty") +
  tm_shape(nat_parks.sf) +
  tm_fill(col = "colour", title = "National parks") +
tm_shape(nat_reserves.sf) +
  tm_dots(col = "colour", alpha = 0.9, size = 0.1, title = "National nature reserves") +
tm_shape(nat_reserves_local.sf) +
  tm_dots(col = "colour", alpha = 0.5, size = 0.1, title = "Local nature reserves") +
  tm_layout(frame = FALSE, legend.show = TRUE)




