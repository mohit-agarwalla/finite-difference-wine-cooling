# Modelling the distribution of a wine bottle inside a wine bottle

_To learn about the origin and submission for this assignment please see Submission.pdf, but please note there have been changes to the code since._

The temperature distribution of wine placed inside a wine cooler of 15°C was investigated over time. The initial temperature of the wine was 25°C and the time taken for all the wine to reach the ideal range of serving temperatures (15 - 16°C). Modelling the cooling distribution of a wine bottle inside a wine cooler with a finite difference method. This was originally created as a product of coursework for second year Computing coursework but ahs since been improved and updated.

The heat diffusion equation, henceforth HDE was solved using a finite difference method (FDM). FDMs solve differential equations by approximating them with difference equations, making this is a simple method. It is efficient in regards to memory handling, as it requires minimal recall of previous objects compared to other methods. As well as simplicity, the finite difference method was chosen as it can easily model irregular shapes, like the wine bottle.

## Next steps
This repository is being updated and so there are items that are still to be done. The next commit looks to have the following changes:
- Refactor code to match pythonic standards and keep the scripts functional
- Make the bottle a more normal shape as compared to the amalgamation of two rectangles
- Accomodate for multiple types of bottle shapes as shown in the image below
- Model the bottle as its own shape instead of being enclosed inside a rectangle

![Wine bottle shapes](img\wine-bottle-shapes.png "Wine Bottle Shapes")

AUTHOR CREDITS: ANYA PARMAR & MOHIT AGARWALLA