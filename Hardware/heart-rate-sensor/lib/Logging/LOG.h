#ifndef LOG_h
#define LOG_h

#include <ArduinoLog.h>

// ---------
#define __LOG_LOGGING_LEVEL LOG_LEVEL_VERBOSE
// ---------

void printLogLevel(Print *_logOutput, int logLevel);
void setupLogging(Print *serial);

#if __LOG_LOGGING_LEVEL >= 5
#define STR_HELPER(x) #x
#define STR(x)        STR_HELPER(x)
#define _LOG_FORMAT   ": [" __FILE__ ":" STR(__LINE__) "] : "
#else
#define _LOG_FORMAT ": "
#endif

#define log_trace(M, ...)   Log.verboseln(_LOG_FORMAT M, ##__VA_ARGS__)
#define log_debug(M, ...)   Log.traceln(_LOG_FORMAT M, ##__VA_ARGS__)
#define log_info(M, ...)    Log.infoln(_LOG_FORMAT M, ##__VA_ARGS__)
#define log_warning(M, ...) Log.warningln(_LOG_FORMAT M, ##__VA_ARGS__)
#define log_error(M, ...)   Log.errorln(_LOG_FORMAT M, ##__VA_ARGS__)
#define log_fatal(M, ...)   Log.fatalln(_LOG_FORMAT M, ##__VA_ARGS__)
#endif

/*
 * NOTE: if function names are needed in future, revert back to "non-clean"
 *       implementation with 2 sets of macros in if-else blocks one having
 *       __FUNCTION__, __LINE__ etc arguments passed to logger, and the other
 *       set simple as what is above
 */
