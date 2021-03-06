import ZeroHour as zerohour
import sys

options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
args    = [arg for arg in sys.argv[1:] if arg not in options]

cmdLineOptions = zerohour.parseCommandLineOptions(options)

zerohour.initTrello(cmdLineOptions)
tBoard = zerohour.getTrelloBoard(cmdLineOptions['trelloID'], cmdLineOptions['trelloToken'], cmdLineOptions['trelloUser'], cmdLineOptions['trelloBoard'])
tList = zerohour.getTrelloList(cmdLineOptions['trelloID'], cmdLineOptions['trelloToken'], tBoard, cmdLineOptions['trelloList'])

rally = zerohour.initRally(cmdLineOptions)

print "Logging changes to change.log..."
changeLog = open("change.log", 'a')

#TODO replace with migrateRallyArtifactsToTrello()
artifactQuery = zerohour.buildRallyArtifactInclusionQuery(rally, cmdLineOptions['trelloID'], cmdLineOptions['trelloToken'], tBoard)
tasksForMigration = zerohour.getRallyRallyArtifactList(rally, artifactQuery, 'migration.list')
trelloCards = zerohour.sortArtifactsIntoTrelloTasks(rally, tasksForMigration)
orderedParentCards = zerohour.orderCards(rally, trelloCards)
zerohour.addTrelloCards(orderedParentCards, trelloCards, cmdLineOptions['trelloID'], cmdLineOptions['trelloToken'], tList, changeLog)

#FINALIZE
changeLog.close()