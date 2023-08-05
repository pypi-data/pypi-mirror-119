// [IGE]: avoid linking to python37_d.lib
#ifdef _DEBUG
#  define IGE_DEBUG
#  undef _DEBUG
#endif

#include <Python.h>

#ifdef IGE_DEBUG
# define _DEBUG
#endif
// [/IGE]

#include "Firebase.h"
#include "FirebaseAnalytics.h"
#include "FirebaseAuth.h"
#include "FirebaseMessaging.h"
#include "FirebaseRemoteConfig.h"
#include "FirebaseMLKit.h"
#include "FirebaseFirestore.h"

typedef struct {
	PyObject_HEAD
		Firebase* firebase;
} firebase_obj;

typedef struct {
	PyObject_HEAD
		FirebaseAnalytics* firebaseAnalytics;
} firebaseAnalytics_obj;

typedef struct {
	PyObject_HEAD
		FirebaseAuth* firebaseAuth;
} firebaseAuth_obj;

typedef struct {
	PyObject_HEAD
		FirebaseMessaging* firebaseMessaging;
} firebaseMessaging_obj;

typedef struct {
	PyObject_HEAD
		FirebaseRemoteConfig* firebaseRemoteConfig;
} firebaseRemoteConfig_obj;

typedef struct {
	PyObject_HEAD
		FirebaseMLKit* firebaseMLKit;
} firebaseMLKit_obj;

typedef struct {
	PyObject_HEAD
		FirebaseFirestore* firebaseFirestore;
} firebaseFirestore_obj;

extern PyTypeObject FirebaseType;
extern PyTypeObject FirebaseAnalyticsType;
extern PyTypeObject FirebaseAuthType;
extern PyTypeObject FirebaseMessagingType;
extern PyTypeObject FirebaseRemoteConfigType;
extern PyTypeObject FirebaseMLKitType;
extern PyTypeObject FirebaseFirestoreType;