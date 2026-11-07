import PBLean.F10.Comax 
import PBLean.F10.Morita 
import PBLean.F10.Dirac 
import PBLean.F10.Gauge 
import PBLean.F10.Filtration 
import PBLean.F10.SmithT0 
import PBLean.F10.BaireN1

/-! Controllo degli assiomi (S10-LEAN): ammessi solo propext, Classical.choice, Quot.sound. -/

#print axioms PBLean.F10.Comax.Sol
#print axioms PBLean.F10.Comax.Sol_antitone
#print axioms PBLean.F10.Comax.Sol_sup
#print axioms PBLean.F10.Comax.sumMap
#print axioms PBLean.F10.Comax.sumMap_apply
#print axioms PBLean.F10.Comax.sumMap_surjective
#print axioms PBLean.F10.Comax.Sol_inf_of_sup_eq_top
#print axioms PBLean.F10.Comax.scalar_case

#print axioms PBLean.F10.Morita.matOp
#print axioms PBLean.F10.Morita.matOp_apply
#print axioms PBLean.F10.Morita.matOp_mul_apply
#print axioms PBLean.F10.Morita.matOp_smul_apply
#print axioms PBLean.F10.Morita.matOp_add_apply
#print axioms PBLean.F10.Morita.matOp_one_apply
#print axioms PBLean.F10.Morita.matEnd
#print axioms PBLean.F10.Morita.Sol
#print axioms PBLean.F10.Morita.rowPair
#print axioms PBLean.F10.Morita.rowEquiv
#print axioms PBLean.F10.Morita.rowSpan
#print axioms PBLean.F10.Morita.rowSpan_le_ker_iff
#print axioms PBLean.F10.Morita.map_Sol_eq
#print axioms PBLean.F10.Morita.solEquiv
#print axioms PBLean.F10.Morita.quotHomEquiv
#print axioms PBLean.F10.Morita.malgrange
#print axioms PBLean.F10.Morita.det_smul_eq_zero_of_mem_Sol
#print axioms PBLean.F10.Morita.end_mul_apply
#print axioms PBLean.F10.Morita.end_kernel_decomposition
#print axioms PBLean.F10.Morita.matrix_kernel_decomposition
#print axioms PBLean.F10.Morita.scalarKer
#print axioms PBLean.F10.Morita.mem_scalarKer
#print axioms PBLean.F10.Morita.sol_split_of_det

#print axioms PBLean.F10.Dirac.sum_mul_self_of_anticomm
#print axioms PBLean.F10.Dirac.clifford_sq
#print axioms PBLean.F10.Dirac.massive_factor
#print axioms PBLean.F10.Dirac.scalar_sub_mul_add
#print axioms PBLean.F10.Dirac.pauli
#print axioms PBLean.F10.Dirac.pauli_sq
#print axioms PBLean.F10.Dirac.pauli_anticomm
#print axioms PBLean.F10.Dirac.Sym
#print axioms PBLean.F10.Dirac.p
#print axioms PBLean.F10.Dirac.pauliR
#print axioms PBLean.F10.Dirac.pauliR_sq
#print axioms PBLean.F10.Dirac.pauliR_anticomm
#print axioms PBLean.F10.Dirac.sigmaDotP
#print axioms PBLean.F10.Dirac.KG
#print axioms PBLean.F10.Dirac.sigmaDotP_sq
#print axioms PBLean.F10.Dirac.Xc
#print axioms PBLean.F10.Dirac.Yc
#print axioms PBLean.F10.Dirac.XY_eq_KG
#print axioms PBLean.F10.Dirac.diracChiral
#print axioms PBLean.F10.Dirac.diracChiral_sq
#print axioms PBLean.F10.Dirac.dirac_massive
#print axioms PBLean.F10.Dirac.antidiag_sq
#print axioms PBLean.F10.Dirac.dirac2_sq

#print axioms PBLean.F10.Gauge.gmul
#print axioms PBLean.F10.Gauge.gmul_apply
#print axioms PBLean.F10.Gauge.nabla
#print axioms PBLean.F10.Gauge.nabla_apply
#print axioms PBLean.F10.Gauge.gaugeTransform
#print axioms PBLean.F10.Gauge.nabla_covariant
#print axioms PBLean.F10.Gauge.op
#print axioms PBLean.F10.Gauge.op_covariant
#print axioms PBLean.F10.Gauge.sol_gauge
#print axioms PBLean.F10.Gauge.invariant_data_gauge
#print axioms PBLean.F10.Gauge.gauge_fixing_u_trivial

#print axioms PBLean.F10.Filtration.kernelAt
#print axioms PBLean.F10.Filtration.Fit
#print axioms PBLean.F10.Filtration.kernelAt_mono
#print axioms PBLean.F10.Filtration.kernelAt_compat
#print axioms PBLean.F10.Filtration.iSup_kernelAt
#print axioms PBLean.F10.Filtration.not_fit_iff
#print axioms PBLean.F10.Filtration.fit_mono
#print axioms PBLean.F10.Filtration.finrank_le_kernelAt_add
#print axioms PBLean.F10.Filtration.Rle
#print axioms PBLean.F10.Filtration.Rle_mono
#print axioms PBLean.F10.Filtration.iSup_Rle
#print axioms PBLean.F10.Filtration.mul_mem_Rle
#print axioms PBLean.F10.Filtration.evAt
#print axioms PBLean.F10.Filtration.iSup_kernelAt_Rle
#print axioms PBLean.F10.Filtration.consequences_le_kernelAt
#print axioms PBLean.F10.Filtration.finrank_Rle_le

#print axioms PBLean.F10.SmithT0.rootCount
#print axioms PBLean.F10.SmithT0.socle_le_one_iff

#print axioms PBLean.F10.BaireN1.interior_eq_empty_of_isCompact
#print axioms PBLean.F10.BaireN1.isMeagre_iUnion_compact
