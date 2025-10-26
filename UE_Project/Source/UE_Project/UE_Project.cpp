#include "UE_Project.h"

#define LOCTEXT_NAMESPACE "FUE_ProjectModule"

void FUE_ProjectModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
}

void FUE_ProjectModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FUE_ProjectModule, UE_Project)