# Latest Information Indonesia Earthquake
Latest information Indonesia earthquake from Meteorological, Climatological, and Geophysical Agency

## How It Work?
This package will scrape from [BMKG](https://bmkg.go.id) to get latest information Indonesia earthquake

This package will use BeautifulSoup4 and Request, can be used to collect the latest data on earthquakes in Indonesia

#How To Use
````
import earthquake_detection

if __name__ == "__main__":
    result = earthquake_detection.ekstraksi_data()
    earthquake_detection.tampilkan_data(result)
````

#Author
Ade Ristanto