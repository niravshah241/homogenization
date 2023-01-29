import dolfinx
import ufl

from mpi4py import MPI
from petsc4py import PETSc

import numpy as np
import matplotlib.pyplot as plt

#Read mesh
gdim = 2
gmsh_model_rank = 0
mesh_comm  = MPI.COMM_WORLD
mesh, cell_tags, facet_tags = dolfinx.io.gmshio.read_from_msh("mesh_data/mesh.msh", mesh_comm, gmsh_model_rank, gdim = gdim)

V = dolfinx.fem.FunctionSpace(mesh,("CG",2))
u, v = ufl.TrialFunction(V), ufl.TestFunction(V)
uh = dolfinx.fem.Function(V)
uh.name = "Temperature"

k1, k2, k3, k4 = 5.5, 5., 5., 5.5 # Thermal conductivity

V2 = dolfinx.fem.FunctionSpace(mesh,("DG",0))

k = dolfinx.fem.Function(V2)

cells_1 = cell_tags.find(1) 
cells_2 = cell_tags.find(2) 
cells_3 = cell_tags.find(3) 
cells_4 = cell_tags.find(4)

k.x.array[cells_1] = np.full_like(cells_1, k1, dtype=PETSc.ScalarType)
k.x.array[cells_2] = np.full_like(cells_2, k2, dtype=PETSc.ScalarType)
k.x.array[cells_3] = np.full_like(cells_3, k3, dtype=PETSc.ScalarType)
k.x.array[cells_4] = np.full_like(cells_4, k4, dtype=PETSc.ScalarType)

a = dolfinx.fem.form(k*ufl.inner(ufl.grad(u),ufl.grad(v)) * ufl.dx)
l = dolfinx.fem.form(ufl.inner(dolfinx.fem.Constant(mesh, PETSc.ScalarType(0.)),v) * ufl.dx)

dofs_bc_4 = dolfinx.fem.locate_dofs_topological(V, gdim-1, facet_tags.find(4))
dofs_bc_6 = dolfinx.fem.locate_dofs_topological(V, gdim-1, facet_tags.find(6))
dofs_bc_10 = dolfinx.fem.locate_dofs_topological(V, gdim-1, facet_tags.find(10))
dofs_bc_11 = dolfinx.fem.locate_dofs_topological(V, gdim-1, facet_tags.find(11))

bc_4 = dolfinx.fem.dirichletbc(PETSc.ScalarType(1500.), dofs_bc_4, V)
bc_10 = dolfinx.fem.dirichletbc(PETSc.ScalarType(1500.), dofs_bc_10, V)
bc_6 = dolfinx.fem.dirichletbc(PETSc.ScalarType(300.), dofs_bc_6, V)
bc_11 = dolfinx.fem.dirichletbc(PETSc.ScalarType(300.), dofs_bc_11, V)

bcs = [bc_4, bc_6, bc_10, bc_11]

temperature_1D_file_xdmf = dolfinx.io.XDMFFile(mesh.comm, "temperature_1D/temperature_1D.xdmf", "w")
temperature_1D_file_xdmf.write_mesh(mesh)

A = dolfinx.fem.petsc.assemble_matrix(a, bcs=bcs)
A.assemble()

F = dolfinx.fem.petsc.assemble_vector(l)
dolfinx.fem.petsc.apply_lifting(F, [a], [bcs])
F.ghostUpdate(addv=PETSc.InsertMode.ADD, mode=PETSc.ScatterMode.REVERSE)
dolfinx.fem.petsc.set_bc(F,bcs)
ksp = PETSc.KSP()
ksp.create(mesh.comm)
ksp.setOperators(A)
ksp.setType("preonly")
ksp.getPC().setType("lu")
ksp.getPC().setFactorSolverType("mumps")
ksp.setFromOptions()
ksp.solve(F, uh.vector)
#uh.vector.ghostUpdate(addv=PETSc.InsertMode.INSERT, mode=PETSc.ScatterMode.FORWARD)
uh.x.scatter_forward()
temperature_1D_file_xdmf.write_function(uh)

q_flux_expr = -k * ufl.grad(uh)
VQ = dolfinx.fem.VectorFunctionSpace(mesh,("CG",1))
q_flux = dolfinx.fem.Expression(q_flux_expr, VQ.element.interpolation_points())
q_flux_func = dolfinx.fem.Function(VQ)
q_flux_func.interpolate(q_flux)
q_flux_func.name = "Heat_flux"
q_flux_func.x.scatter_forward()
temperature_1D_file_xdmf.write_function(q_flux_func)
