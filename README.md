# **Sawatch iOS Telemetry Data Report**

## Jane Stout
#### 2 December 2018

This report provides an analysis of N = 1000 instances of trip information for five vehicles colleted via iOS telemetry. My goal was to explore and visualize patterns in the data and ultimately build a model that would predict fuel usage. Table 1 presents variables used in my analysis.

**Table 1. Variable Labels and Definitions Used in the Current Analysis**

| Variable label          | Definition |
|-------------------------|-----------------|
| fuel_used (Target)      | Liters of fuel used since last report           |
| kmph                    | Kilometers per hour (i.e., speed)         |
| celsius                 | Ambient air temperature            |
| altitude_delta          | Delta in meters between last altitude report and current            |
| g_force                 | Calculated g net gravity            |
| kml                     | Kilometers per liter          |
| kilometers              | Kilometers since last report          |
| weather_type_Bad        | Ambient weather was Bad (1: *mist, overcast clouds, broken clouds*) or Good (0: *few clouds, clear sky*)           |
| vehicle_type            | Vehicle Type: SUV (1) or Sedan (0)            |
| latitude                | Degrees latitude          |
| longitude               | Degrees longitude            |

#### Geospatial Analysis

I first plotted latitude and longitude coordinates for each datapoint in the dataset (the code is found [here](geoplotting.py)). As seen in Figure 1, there were five distinct data collection locations.

**Figure 1. Geospatial Data Collection Locations**

![](images/geomap_cropped.png)

*Note.* Red dots represent data collection locations.

#### Exporatory Data Analysis

Figure 2 displays a scatter matrix containing (a) correlations between continuous variables (excluding latitude and longtiude) and (b) histograms for each variable along the diagonal. As seen in the histograms, several variables contained a large number of zero values. These zero values correspond to instances where vehicles were idle (e.g., at a stop light). Scatterplots also point to some clearly co-linear relationships. For instance, kilometers since last report (kilometers) and kilometers per hour (kmph) have nearly a 1:1 relationship. This will become relevant during the modeling phase of my analysis.

**Figure 2. Scatter Matrix of Continuous Variables**

![](images/scatmatrix.png)

Figure 3 displays fuel usage as a function of whether the weather was bad (e.g., cloudy; misty) or good (e.g., sunny) at each time of data collection. Here, we see greater fuel usage when the weather is good.

**Figure 3. Average Fuel Usage by Weather Type**

![](images/weather.png)

Figure 4 displays fuel usage as a function of the type of vehicle: SUV vs. Sedan. This figure shows, in this particular sample, Sedans used more fuel, on average, than SUVs.

**Figure 4. Average Fuel Usage by Vehicle Type**

![](images/veh_type.png)

Next, I built a mulitple linear regression model where I regressed *fuel_used* on *kmph, celsius, altitude_delta, g_force, kml, weather_type,* and *vehicle_type*. Note that, given the strong relationship between kmph and kilometers (see Figure 1), I omitted kilometers from the model.

I first split the full dataset into training and testing data (75% and 25% of the full dataset, respectively) and assessed colinearity, if any, among features in the model. To do so I observed Variance Inflation Factors (VIFs) among all of the features. VIF values of >10 indicate a given feature is extremely correlated with other features, which may result in an unreliable model. As seen in Table 2, the VIFs were all acceptable (<10).

**Table 2. VIFs for Features in Model**

| Variable label          | VIF coefficient |
|-------------------------|-----------------|
| kmph                    | 9.65            |
| celsius                 | 3.15            |
| altitude_delta          | 1.30            |
| g_force                 | 1.83            |
| kml                     | 9.87            |
| weather_type            | 3.63            |
| vehicle_type            | 4.37            |

Next, I assessed heteroscedasticity of the model residuals by plotting a scatterplot of the predicted values and the residuals (see Figure 5). Residuals were reasonably homoscadastic (distributed evenly), though there is evidence of some outliers in the model fit (i.e., scatter dots that notably deviate in the positive/negative direction of the y axis).

**Figure 5. Scatterplot of Predicted Values Versus Residuals**

![](images/Resids_Training.png)

Next, I compared my model for training versus testing data. Table 3 displays model fit information and coefficients.

As seen in Table 3, the training and tesing data both fit the model well (Adjusted R-squareds >= .76). Given the small absolute amount of fuel usages per trip, *b* coefficients are difficult to interpret. However, *t* statistics provide a measure of the strength of the effects and the *p* values indicate whether each effect was statistically significant. The following is an interpretation of coefficients for the tesing model:

- Higher vehicle speed (kpmh) predicts significantly greater fuel usage; this is a strong predictor
- Higher ambient air temperature (celsius) significantly predicts less fuel usage; this is a relatively weak predictor
- As elevation level rises (altitude_delta), fuel usage also rises significantly
- As g net gravity increases (g_force), fuel usage also increses; this is a relatively weak predictor
- More kilometers per liter (kml) are associated with less fuel usage
- Outdoor weather (weather_type) does not reliably predict fuel usage
- Whether a vehicle is a SUV versus Sedan (vehicle_type) does not reliably predict fuel usage


**Table 3. Fit statistics and Coefficients for Testing Versus Training Regression Models**

![](images/Table3.jpg)
<!--
|                <td colspan='5'><b><center> Training Model <td colspan='5'><b><center> Testing Model |
|----------------|----------------|---------|----------|---------|---------|----------------|---------|----------|---------|---------|
|                | <b><i>Adj. R-squared       | <b><i>b | <b><i>SE | <b><i>t | <b><i>p | <b><i>Adj. R-squared | <b><i>b | <b><i>SE | <b><i>t | <b><i>p |
|                | .76            |         |          |         |         | .83            |         |          |         |         |
| constant       |                |   .003  |  .000    |  18.34  | <.001   |                |   .003  | <.001    |  13.48  | <.001   |
| kmph           |                |  <.001  | <.001    |  33.26  | <.001   |                |  <.001  | <.001    |  22.79  | <.001   |
| celsius        |                | <-.001  | <.001    |  -5.53  | <.001   |                | <-.001  | <.001    |  -3.10  |  .002   |
| altitude_delta |                |   .001  | <.001    |   9.85  | <.001   |                |   .001  | <.001    |   6.82  | <.001   |
| g_force        |                |   .002  | <.001    |   4.94  | <.001   |                |   .002  |  .001    |   3.96  | <.001   |
| kml            |                | <-.001  | <.001    | -16.12  | <.001   |                | <-.001  | <.001    | -11.22  | <.001   |
| weather_type   |                | <-.001  | <.001    | -2.04   |  .04    |                | <-.001  | <.001    |  -0.72  |   .47   |
| vehicle_type   |                |   .001  | <.001    |   5.37  | <.001   |                |  <.001  | <.001    |   1.60  |   .11   |           
 -->

#### Future Directions

In the future, I would like to anlayze telemetric data for electric vehicles to gauge battery efficieny. My personal experience with electric vehicles is that battery life degrades quickly in cold weather and at high speeds. I wonder what other telemetrics can address this type of research question.

It would also be interesting to compare fuel versus battery efficiency for gas-powered versus electric vehicles in terms of financial cost. For instance, given the same distance traveled, same altitude change, etc, which car is more expensive to drive (i.e., cost of fuel versus cost of electricty to charge battery)?

In summary, telemetrics provide an exciting data source that can address practical research questions for the fleet industry.
