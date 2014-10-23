orchid_addons
=============
Sale_ Target & Purchase Plan

24-10-2014 - Fakrudeen

Modules
Sales > Sales Forecast
Purchase > Purchase Plan
Reports
Reports > Sales > Sales Target
Reports > Purchase > Paurchase Plan

Steps to use Sales Target
Name, Company & Price list
Branch (ware house - optional)
Fiscal Year and Period is used to link actual sales - Its planned to link with sales invoice not sales orders - link will be with period id in account_invoice 
Sales History
Monthly - Taking previous months from From date (number of months from sale avarage) 
3 month average with date from 01-01-2014  will be sales of  [ October 2013+November 2013+ December 2013 ] / 3 = average monthly sale
Yearly  - not implmented (concept is taking same month from the last years to get  seasonal effect ) Not implmented its an advanced model
Taking average of same month in the lastr year means - for sales target of Jan 2014 with average of 3 months 
Sales of ( Jan 2011+Jan2012+Jan2013 ) / 3 = Average sale 
Target Factor - Sales increase or decrease effect - means from monthly sales average willbe multiple with targer factor - its sales trend upword or downword.
Estimated Target is figure management expecitng (its a value to start with - no effect any where)
Planned Target is the final valu arrived after process 
Achieved is actual sales
Then go to generate
Its will navigate to calculate sale average
Then process
Calculate sale avaerage for a month - qty- sale amount - average price
Options to generate sales target - Brand wise - Customer wise etc..
Product wise is the best method and its only keeping quantity wise target, other options just keep value
Then Back button
go back to main screen
Then Distribute
To generate initial target based on the sales target
Computed amount is the total of the lines
Sales Target object have 12 Qty collumns and 12 Amount collumns- its taking average price to calculate value
any fraction of quantity will be rounded off to upper side
Then Edit lines
Edit lines to give seasonal effect like off season sale or festival season sale etc...
Then Generate purhase plan 
Lead time wise - it will take minimum lead time from product master supplier
Price wise - it will take minimum price from the product master supplier
Purchase Plan object have 12 Qty collumns and 12 Amount collumns- its taking price and lead time from the product master supplier
