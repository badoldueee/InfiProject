#ifndef INFI_LIB_H
#define INFI_LIB_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>

/* Global Configuration Flags for Compiler Context */
static int INFI_SIMULATION_MODE = 0;

/* Helper: Get Current System Date */
void get_now(char* buffer) {
    time_t t = time(NULL);
    struct tm *tm = localtime(&t);
    strftime(buffer, 20, "%Y-%m-%d", tm);
}

/* Helper: Safety Check to Skip Operating System Root Pointers */
int is_system_pointer(const char* name) {
    return (strcmp(name, ".") == 0 || strcmp(name, "..") == 0);
}

/* Helper: Check if a path is a regular file (Cross-Platform Windows Fix) */
int is_regular_file(const char *path) {
    struct stat path_stat;
    if (stat(path, &path_stat) != 0) return 0;
    return S_ISREG(path_stat.st_mode);
}

/* Enable Simulation Dry-Run Mode */
void infi_enable_simulation() {
    INFI_SIMULATION_MODE = 1;
    printf("[Infi System] >>> SIMULATION MODE ENABLED. No physical disk changes will be made. <<<\n");
}

/* Disable Simulation Mode */
void infi_disable_simulation() {
    INFI_SIMULATION_MODE = 0;
}

/* LEVEL 1: STANDARD C FILE OPERATIONS */

void create_folder(const char* name) {
    printf("[Infi Action] create_folder(\"%s\")\n", name);
    if (INFI_SIMULATION_MODE) return;
    
    #ifdef _WIN32
        mkdir(name);
    #else
        mkdir(name, 0777);
    #endif
}

void write_file(const char* name, const char* content) {
    printf("[Infi Action] write_file(\"%s\") -> Contents injected.\n", name);
    if (INFI_SIMULATION_MODE) return;

    FILE *f = fopen(name, "w");
    if (f) {
        fprintf(f, "%s", content);
        fclose(f);
    }
}

void copy_file(const char* source, const char* dest) {
    printf("[Infi Action] copy_file: \"%s\" to \"%s\"\n", source, dest);
    if (INFI_SIMULATION_MODE) return;

    FILE *src = fopen(source, "rb");
    FILE *dst = fopen(dest, "wb");
    if (!src || !dst) {
        if (src) fclose(src);
        if (dst) fclose(dst);
        return;
    }
    char buffer[4096];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        fwrite(buffer, 1, bytes, dst);
    }
    fclose(src);
    fclose(dst);
}

void move_file(const char* source, const char* dest) {
    printf("[Infi Action] move_file: \"%s\" to \"%s\"\n", source, dest);
    if (INFI_SIMULATION_MODE) return;
    rename(source, dest);
}

void delete_single(const char* name) {
    printf("[Infi Action] delete_single: \"%s\"\n", name);
    if (INFI_SIMULATION_MODE) return;
    remove(name);
}

/* LEVEL 2: DIRECTORY BATCH AUTOMATION ENGINE */

void bulk_prefix(const char* prefix) {
    DIR *d = opendir(".");
    struct dirent *dir;
    if (!d) return;

    while ((dir = readdir(d)) != NULL) {
        if (!is_system_pointer(dir->d_name) && is_regular_file(dir->d_name)) {
            char newname[512];
            snprintf(newname, sizeof(newname), "%s%s", prefix, dir->d_name);
            printf("[Infi Batch] Rename: \"%s\" -> \"%s\"\n", dir->d_name, newname);
            if (!INFI_SIMULATION_MODE) rename(dir->d_name, newname);
        }
    }
    closedir(d);
}

void bulk_suffix(const char* suffix) {
    DIR *d = opendir(".");
    struct dirent *dir;
    if (!d) return;

    while ((dir = readdir(d)) != NULL) {
        if (!is_system_pointer(dir->d_name) && is_regular_file(dir->d_name)) {
            char newname[512];
            char name_copy[256];
            strcpy(name_copy, dir->d_name);
            char *dot = strrchr(name_copy, '.');
            
            if (dot) {
                *dot = '\0';
                snprintf(newname, sizeof(newname), "%s%s.%s", name_copy, suffix, dot + 1);
            } else {
                snprintf(newname, sizeof(newname), "%s%s", dir->d_name, suffix);
            }
            printf("[Infi Batch] Rename: \"%s\" -> \"%s\"\n", dir->d_name, newname);
            if (!INFI_SIMULATION_MODE) rename(dir->d_name, newname);
        }
    }
    closedir(d);
}

void delete_if_match(const char* phrase) {
    DIR *d = opendir(".");
    struct dirent *dir;
    if (!d) return;

    while ((dir = readdir(d)) != NULL) {
        if (!is_system_pointer(dir->d_name) && is_regular_file(dir->d_name)) {
            if (strstr(dir->d_name, phrase)) {
                printf("[Infi Batch] Purge Target Found: \"%s\"\n", dir->d_name);
                if (!INFI_SIMULATION_MODE) remove(dir->d_name);
            }
        }
    }
    closedir(d);
}

void archive_others(const char* keep_name) {
    DIR *d = opendir(".");
    struct dirent *dir;
    char date[20];
    get_now(date);
    if (!d) return;

    while ((dir = readdir(d)) != NULL) {
        if (!is_system_pointer(dir->d_name) && is_regular_file(dir->d_name)) {
            if (strcmp(dir->d_name, keep_name) == 0) continue;
            
            char newname[512];
            snprintf(newname, sizeof(newname), "OLD_%s_%s", date, dir->d_name);
            printf("[Infi Batch] Archive Relocation: \"%s\" -> \"%s\"\n", dir->d_name, newname);
            if (!INFI_SIMULATION_MODE) rename(dir->d_name, newname);
        }
    }
    closedir(d);
}

/* LEVEL 3: ADVANCED ENTERPRISE SECURITY & DEEP CONTENT INSPECTION */

void encrypt_file(const char* filename, const char* key) {
    printf("[Infi Security] Encrypting/Decrypting File: \"%s\" with cipher key stream.\n", filename);
    if (INFI_SIMULATION_MODE) return;

    FILE *f = fopen(filename, "rb+");
    if (!f) return;

    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    rewind(f);

    char *buffer = (char *)malloc(size);
    if (buffer) {
        fread(buffer, 1, size, f);
        size_t key_len = strlen(key);
        
        for (long i = 0; i < size; i++) {
            buffer[i] ^= key[i % key_len];
        }
        
        rewind(f);
        fwrite(buffer, 1, size, f);
        free(buffer);
    }
    fclose(f);
}

unsigned long calculate_file_hash(const char* filename) {
    if (INFI_SIMULATION_MODE) {
        printf("[Infi Security] Hash calculation mocked for simulation.\n");
        return 0;
    }
    FILE *f = fopen(filename, "rb");
    if (!f) return 0;

    unsigned long hash = 5381;
    int c;
    while ((c = fgetc(f)) != EOF) {
        hash = ((hash << 5) + hash) + c;
    }
    fclose(f);
    return hash;
}

void scan_content_for_phrase(const char* pattern, const char* phrase) {
    DIR *d = opendir(".");
    struct dirent *dir;
    if (!d) return;

    while ((dir = readdir(d)) != NULL) {
        if (!is_system_pointer(dir->d_name) && is_regular_file(dir->d_name) && strstr(dir->d_name, pattern)) {
            FILE *f = fopen(dir->d_name, "r");
            if (f) {
                char line_buf[1024];
                int line_num = 1;
                while (fgets(line_buf, sizeof(line_buf), f)) {
                    if (strstr(line_buf, phrase)) {
                        printf("[Infi Deep-Scan] Found match in \"%s\" (Line %d): %s", dir->d_name, line_num, line_buf);
                    }
                    line_num++;
                }
                fclose(f);
            }
        }
    }
    closedir(d);
}

#endif