import boto3

dynamo_client = boto3.client('dynamodb')
tableName = "smpd_399_timestamp"


def showTable():
    return dynamo_client.scan(TableName=tableName)


def getValues1(column):

    tableFull = dynamo_client.scan(TableName=tableName)
    stringReportedVals = []
    reportedVals = []

    for value in tableFull['Items']:
        stringReportedVals.append(value[column])

    for value in stringReportedVals:
        value = str(value)
        number = ''

        for char in value:
            number += onlyDigits(char)

        reportedVals.append(int(float(number)))

    return reportedVals


def getValues2(column):

    tableFull = dynamo_client.scan(TableName=tableName)
    stringVals = []
    vals = []

    for value in tableFull['Items']:
        stringVals.append(value[column].values())

    for value in stringVals:
        number = ''

        for char in value:
            number += onlyDigits(char)

        vals.append(int(number))

    return vals


def onlyDigits(char):

    for i in range(10):

        if char==str(i):
            return char

    if char=='.':
        return char

    return ''


def orderVals(listArg):
    list = []
    index = 0
    ordered = []

    for item in listArg:
        list.append(item)

    while len(ordered) < len(list):
       smallest = list[0]
       index = 0

       for i in range(len(list)):
           if smallest > list[i]:
               smallest = list[i]
               index = i

       ordered.append(index)
       list[index] = 10000000000000

    return ordered
