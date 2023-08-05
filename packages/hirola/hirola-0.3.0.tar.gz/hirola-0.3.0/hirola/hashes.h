// -*- coding: utf-8 -*-
// Header file generated automatically by cslug.
// Do not modify this file directly as your changes will be overwritten.

#ifndef HASHES_H
#define HASHES_H

#include <stddef.h>
#include <stdint.h>

// hashes.c
int32_t hash(void * key, const size_t key_size);
int32_t small_hash(void * key, const size_t key_size);
int32_t hybrid_hash(void * key, const size_t key_size);

#endif
