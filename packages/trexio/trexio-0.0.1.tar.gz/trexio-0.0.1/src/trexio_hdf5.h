/* This file was generated from the org-mode file.
   To generate it, open templator_hdf5.org file in Emacs and execute
   M-x org-babel-tangle
*/

#ifndef TREXIO_HDF5_H
#define TREXIO_HDF5_H

#include "trexio.h"
#include "trexio_private.h"
#include "trexio_s.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <sys/stat.h>

#include "hdf5.h"
#include "hdf5_hl.h"
typedef struct trexio_hdf5_s {
  trexio_t     parent ;
  hid_t        file_id;
  hid_t        metadata_group;
  hid_t        electron_group;
  hid_t        nucleus_group;
  hid_t        ecp_group;
  hid_t        basis_group;
  hid_t        ao_group;
  hid_t        ao_1e_int_group;
  hid_t        ao_2e_int_group;
  hid_t        mo_group;
  hid_t        mo_1e_int_group;
  hid_t        mo_2e_int_group;
} trexio_hdf5_t;

trexio_exit_code trexio_hdf5_init(trexio_t* const file);
trexio_exit_code trexio_hdf5_deinit(trexio_t* const file);

trexio_exit_code trexio_hdf5_has_metadata_package_version (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_metadata_package_version (trexio_t* const file, char* const str, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_metadata_package_version(trexio_t* const file, const char* str);

trexio_exit_code trexio_hdf5_has_metadata_description (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_metadata_description (trexio_t* const file, char* const str, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_metadata_description(trexio_t* const file, const char* str);

trexio_exit_code trexio_hdf5_has_nucleus_point_group (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_nucleus_point_group (trexio_t* const file, char* const str, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_nucleus_point_group(trexio_t* const file, const char* str);

trexio_exit_code trexio_hdf5_has_basis_type (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_type (trexio_t* const file, char* const str, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_basis_type(trexio_t* const file, const char* str);

trexio_exit_code trexio_hdf5_has_mo_type (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_type (trexio_t* const file, char* const str, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_mo_type(trexio_t* const file, const char* str);

trexio_exit_code trexio_hdf5_has_nucleus_charge(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_nucleus_charge(trexio_t* const file, double* const nucleus_charge, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_nucleus_charge(trexio_t* const file, const double* nucleus_charge, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_nucleus_coord(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_nucleus_coord(trexio_t* const file, double* const nucleus_coord, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_nucleus_coord(trexio_t* const file, const double* nucleus_coord, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_lmax_plus_1(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_lmax_plus_1(trexio_t* const file, int64_t* const ecp_lmax_plus_1, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_lmax_plus_1(trexio_t* const file, const int64_t* ecp_lmax_plus_1, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_z_core(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_z_core(trexio_t* const file, double* const ecp_z_core, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_z_core(trexio_t* const file, const double* ecp_z_core, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_local_n(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_local_n(trexio_t* const file, int64_t* const ecp_local_n, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_local_n(trexio_t* const file, const int64_t* ecp_local_n, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_local_exponent(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_local_exponent(trexio_t* const file, double* const ecp_local_exponent, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_local_exponent(trexio_t* const file, const double* ecp_local_exponent, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_local_coef(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_local_coef(trexio_t* const file, double* const ecp_local_coef, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_local_coef(trexio_t* const file, const double* ecp_local_coef, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_local_power(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_local_power(trexio_t* const file, int64_t* const ecp_local_power, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_local_power(trexio_t* const file, const int64_t* ecp_local_power, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_non_local_n(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_non_local_n(trexio_t* const file, int64_t* const ecp_non_local_n, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_non_local_n(trexio_t* const file, const int64_t* ecp_non_local_n, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_non_local_exponent(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_non_local_exponent(trexio_t* const file, double* const ecp_non_local_exponent, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_non_local_exponent(trexio_t* const file, const double* ecp_non_local_exponent, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_non_local_coef(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_non_local_coef(trexio_t* const file, double* const ecp_non_local_coef, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_non_local_coef(trexio_t* const file, const double* ecp_non_local_coef, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ecp_non_local_power(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_non_local_power(trexio_t* const file, int64_t* const ecp_non_local_power, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ecp_non_local_power(trexio_t* const file, const int64_t* ecp_non_local_power, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_nucleus_index(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_nucleus_index(trexio_t* const file, int64_t* const basis_nucleus_index, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_nucleus_index(trexio_t* const file, const int64_t* basis_nucleus_index, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_nucleus_shell_num(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_nucleus_shell_num(trexio_t* const file, int64_t* const basis_nucleus_shell_num, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_nucleus_shell_num(trexio_t* const file, const int64_t* basis_nucleus_shell_num, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_shell_ang_mom(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_shell_ang_mom(trexio_t* const file, int64_t* const basis_shell_ang_mom, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_shell_ang_mom(trexio_t* const file, const int64_t* basis_shell_ang_mom, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_shell_prim_num(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_shell_prim_num(trexio_t* const file, int64_t* const basis_shell_prim_num, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_shell_prim_num(trexio_t* const file, const int64_t* basis_shell_prim_num, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_shell_factor(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_shell_factor(trexio_t* const file, double* const basis_shell_factor, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_shell_factor(trexio_t* const file, const double* basis_shell_factor, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_shell_prim_index(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_shell_prim_index(trexio_t* const file, int64_t* const basis_shell_prim_index, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_shell_prim_index(trexio_t* const file, const int64_t* basis_shell_prim_index, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_exponent(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_exponent(trexio_t* const file, double* const basis_exponent, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_exponent(trexio_t* const file, const double* basis_exponent, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_coefficient(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_coefficient(trexio_t* const file, double* const basis_coefficient, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_coefficient(trexio_t* const file, const double* basis_coefficient, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_basis_prim_factor(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_prim_factor(trexio_t* const file, double* const basis_prim_factor, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_basis_prim_factor(trexio_t* const file, const double* basis_prim_factor, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_shell(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_shell(trexio_t* const file, int64_t* const ao_shell, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_shell(trexio_t* const file, const int64_t* ao_shell, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_normalization(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_normalization(trexio_t* const file, double* const ao_normalization, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_normalization(trexio_t* const file, const double* ao_normalization, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_1e_int_overlap(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_1e_int_overlap(trexio_t* const file, double* const ao_1e_int_overlap, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_1e_int_overlap(trexio_t* const file, const double* ao_1e_int_overlap, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_1e_int_kinetic(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_1e_int_kinetic(trexio_t* const file, double* const ao_1e_int_kinetic, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_1e_int_kinetic(trexio_t* const file, const double* ao_1e_int_kinetic, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_1e_int_potential_n_e(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_1e_int_potential_n_e(trexio_t* const file, double* const ao_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_1e_int_potential_n_e(trexio_t* const file, const double* ao_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_1e_int_ecp_local(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_1e_int_ecp_local(trexio_t* const file, double* const ao_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_1e_int_ecp_local(trexio_t* const file, const double* ao_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_1e_int_ecp_non_local(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_1e_int_ecp_non_local(trexio_t* const file, double* const ao_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_1e_int_ecp_non_local(trexio_t* const file, const double* ao_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_1e_int_core_hamiltonian(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_1e_int_core_hamiltonian(trexio_t* const file, double* const ao_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_1e_int_core_hamiltonian(trexio_t* const file, const double* ao_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_2e_int_eri(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_2e_int_eri(trexio_t* const file, double* const ao_2e_int_eri, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_2e_int_eri(trexio_t* const file, const double* ao_2e_int_eri, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_ao_2e_int_eri_lr(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_2e_int_eri_lr(trexio_t* const file, double* const ao_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_ao_2e_int_eri_lr(trexio_t* const file, const double* ao_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_coefficient(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_coefficient(trexio_t* const file, double* const mo_coefficient, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_coefficient(trexio_t* const file, const double* mo_coefficient, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_occupation(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_occupation(trexio_t* const file, double* const mo_occupation, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_occupation(trexio_t* const file, const double* mo_occupation, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_1e_int_overlap(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_1e_int_overlap(trexio_t* const file, double* const mo_1e_int_overlap, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_1e_int_overlap(trexio_t* const file, const double* mo_1e_int_overlap, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_1e_int_kinetic(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_1e_int_kinetic(trexio_t* const file, double* const mo_1e_int_kinetic, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_1e_int_kinetic(trexio_t* const file, const double* mo_1e_int_kinetic, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_1e_int_potential_n_e(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_1e_int_potential_n_e(trexio_t* const file, double* const mo_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_1e_int_potential_n_e(trexio_t* const file, const double* mo_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_1e_int_ecp_local(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_1e_int_ecp_local(trexio_t* const file, double* const mo_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_1e_int_ecp_local(trexio_t* const file, const double* mo_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_1e_int_ecp_non_local(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_1e_int_ecp_non_local(trexio_t* const file, double* const mo_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_1e_int_ecp_non_local(trexio_t* const file, const double* mo_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_1e_int_core_hamiltonian(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_1e_int_core_hamiltonian(trexio_t* const file, double* const mo_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_1e_int_core_hamiltonian(trexio_t* const file, const double* mo_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_2e_int_eri(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_2e_int_eri(trexio_t* const file, double* const mo_2e_int_eri, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_2e_int_eri(trexio_t* const file, const double* mo_2e_int_eri, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_2e_int_eri_lr(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_2e_int_eri_lr(trexio_t* const file, double* const mo_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims);
trexio_exit_code trexio_hdf5_write_mo_2e_int_eri_lr(trexio_t* const file, const double* mo_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_metadata_code(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_metadata_code(trexio_t* const file, char* const metadata_code, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_metadata_code(trexio_t* const file, const char** metadata_code, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_metadata_author(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_metadata_author(trexio_t* const file, char* const metadata_author, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_metadata_author(trexio_t* const file, const char** metadata_author, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_nucleus_label(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_nucleus_label(trexio_t* const file, char* const nucleus_label, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_nucleus_label(trexio_t* const file, const char** nucleus_label, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_class(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_class(trexio_t* const file, char* const mo_class, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_mo_class(trexio_t* const file, const char** mo_class, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_mo_symmetry(trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_symmetry(trexio_t* const file, char* const mo_symmetry, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len);
trexio_exit_code trexio_hdf5_write_mo_symmetry(trexio_t* const file, const char** mo_symmetry, const uint32_t rank, const uint64_t* dims);

trexio_exit_code trexio_hdf5_has_metadata_code_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_metadata_code_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_metadata_code_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_metadata_author_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_metadata_author_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_metadata_author_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_electron_up_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_electron_up_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_electron_up_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_electron_dn_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_electron_dn_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_electron_dn_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_nucleus_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_nucleus_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_nucleus_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_ecp_local_num_n_max (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_local_num_n_max (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_ecp_local_num_n_max(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_ecp_non_local_num_n_max (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ecp_non_local_num_n_max (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_ecp_non_local_num_n_max(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_basis_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_basis_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_basis_prim_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_basis_prim_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_basis_prim_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_ao_cartesian (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_cartesian (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_ao_cartesian(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_ao_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_ao_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_ao_num(trexio_t* const file, const uint64_t num);

trexio_exit_code trexio_hdf5_has_mo_num (trexio_t* const file);
trexio_exit_code trexio_hdf5_read_mo_num (trexio_t* const file, uint64_t* const num);
trexio_exit_code trexio_hdf5_write_mo_num(trexio_t* const file, const uint64_t num);

#endif
