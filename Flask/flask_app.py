from flask import Flask, jsonify, render_template
import aws_controller
import json
import datetime as dt

app = Flask(__name__)

@app.route('/')
def dataReadableAll():

    reportedDataUnordered = aws_controller.getValues1('reported_at')
    orderList = aws_controller.orderVals(reportedDataUnordered)

    soilDataUnordered = aws_controller.getValues2('soil_moisture')
    tempDataUnordered = aws_controller.getValues1('temperature')
    humDataUnordered = aws_controller.getValues1('humidity')
    rainDataUnordered = aws_controller.getValues1('rainwater')

    reportedData = []
    soilData = []
    tempData = []
    humData = []
    rainData = []
    isoData = []

    for i in range(len(orderList)):
        reportedData.append(str(reportedDataUnordered[orderList[i]]))
        soilData.append(soilDataUnordered[orderList[i]])
        tempData.append(tempDataUnordered[orderList[i]])
        humData.append(humDataUnordered[orderList[i]])
        rainData.append(rainDataUnordered[orderList[i]])
        isoData.append(str(dt.datetime.utcfromtimestamp(reportedDataUnordered[orderList[i]]).isoformat()))

#    reportedData = []
#    soilData = []
#    tempData = []
#    humData = []
#    rainData = []
#    isoData = []
#    for i in range(72):
#        reportedData.append(i)
#        soilData.append(i)
#        tempData.append(i)
#        humData.append(i)
#        rainData.append(i)
#        isoData.append(i)

    return render_template('home.html', isoData = isoData, soilData = soilData, tempData = tempData, humData = humData, rainData = rainData)

@app.route('/day')
def dataReadableDay():

    reportedDataUnordered = aws_controller.getValues1('reported_at')
    orderList = aws_controller.orderVals(reportedDataUnordered)

    soilDataUnordered = aws_controller.getValues2('soil_moisture')
    tempDataUnordered = aws_controller.getValues1('temperature')
    humDataUnordered = aws_controller.getValues1('humidity')
    rainDataUnordered = aws_controller.getValues1('rainwater')

    reportedData = []
    soilData = []
    tempData = []
    humData = []
    rainData = []
    isoData = []

    transmissions = 71
    if len(orderList) < 71:
        transmissions = len(orderList)

    for i in range(transmissions):
        reportedData.append(str(reportedDataUnordered[orderList[i]]))
        soilData.append(soilDataUnordered[orderList[i]])
        tempData.append(tempDataUnordered[orderList[i]])
        humData.append(humDataUnordered[orderList[i]])
        rainData.append(rainDataUnordered[orderList[i]])
        isoData.append(str(dt.datetime.utcfromtimestamp(reportedDataUnordered[orderList[i]]).isoformat()))

    return render_template('home.html', isoData = isoData, soilData = soilData, tempData = tempData, humData = humData, rainData = rainData)

@app.route('/week')
def dataReadableWeek():

    reportedDataUnordered = aws_controller.getValues1('reported_at')
    orderList = aws_controller.orderVals(reportedDataUnordered)

    soilDataUnordered = aws_controller.getValues2('soil_moisture')
    tempDataUnordered = aws_controller.getValues1('temperature')
    humDataUnordered = aws_controller.getValues1('humidity')
    rainDataUnordered = aws_controller.getValues1('rainwater')

    reportedData = []
    soilData = []
    tempData = []
    humData = []
    rainData = []
    isoData = []

    transmissions = 497
    if len(orderList) < 497:
        transmissions = len(orderList)

    for i in range(transmissions):
        reportedData.append(str(reportedDataUnordered[orderList[i]]))
        soilData.append(soilDataUnordered[orderList[i]])
        tempData.append(tempDataUnordered[orderList[i]])
        humData.append(humDataUnordered[orderList[i]])
        rainData.append(rainDataUnordered[orderList[i]])
        isoData.append(str(dt.datetime.utcfromtimestamp(reportedDataUnordered[orderList[i]]).isoformat()))

    return render_template('home.html', isoData = isoData, soilData = soilData, tempData = tempData, humData = humData, rainData = rainData)

@app.route('/month')
def dataReadableMonth():

    reportedDataUnordered = aws_controller.getValues1('reported_at')
    orderList = aws_controller.orderVals(reportedDataUnordered)

    soilDataUnordered = aws_controller.getValues2('soil_moisture')
    tempDataUnordered = aws_controller.getValues1('temperature')
    humDataUnordered = aws_controller.getValues1('humidity')
    rainDataUnordered = aws_controller.getValues1('rainwater')

    reportedData = []
    soilData = []
    tempData = []
    humData = []
    rainData = []
    isoData = []

    transmissions = 2130
    if len(orderList) < 2130:
        transmissions = len(orderList)

    for i in range(transmissions):
        reportedData.append(str(reportedDataUnordered[orderList[i]]))
        soilData.append(soilDataUnordered[orderList[i]])
        tempData.append(tempDataUnordered[orderList[i]])
        humData.append(humDataUnordered[orderList[i]])
        rainData.append(rainDataUnordered[orderList[i]])
        isoData.append(str(dt.datetime.utcfromtimestamp(reportedDataUnordered[orderList[i]]).isoformat()))

    return render_template('home.html', isoData = isoData, soilData = soilData, tempData = tempData, humData = humData, rainData = rainData)

if __name__ == "__main__":
    app.run(debug=True)
