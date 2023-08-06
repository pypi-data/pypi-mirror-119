git clone --depth 1 -b v2.8.0 https://gitlab.dune-project.org/staging/dune-typetree
git clone --depth 1 -b v2.8.0 https://gitlab.dune-project.org/staging/dune-functions

git clone https://git.imp.fu-berlin.de/agnumpde/dune-matrix-vector.git
cd dune-matrix-vector
git reset --hard 7e464f73a77dfb721bc168f87f29d0aab61cc0bf
cd ..
git clone https://git.imp.fu-berlin.de/agnumpde/dune-solvers.git
cd dune-solvers
git reset --hard 5849f018caa2e48befc7e3693191596661b7340d
cd ..
git clone https://git.imp.fu-berlin.de/agnumpde/dune-tnnmg.git
cd dune-tnnmg
git reset --hard 1fbd2501f2332a613b49531f4c50d26777ad200e
cd ..

git clone https://git.imp.fu-berlin.de/agnumpde/dune-fufem.git
cd dune-fufem
git reset --hard 97e1601537bad2dbf5718ee82c22346d01216614
cp ../patches/transferoperatorassembler.hh dune/fufem/assemblers/transferoperatorassembler.hh
cd ..

install_prefix=$1

build() {
mkdir build
cd build
cmake .. -G Ninja -DCMAKE_INSTALL_PREFIX:PATH=$install_prefix\
  -DSKBUILD:BOOL=TRUE\
  -DBUILD_SHARED_LIBS=TRUE\
  -DUSE_PTHREADS=ON\
  -DCMAKE_BUILD_TYPE=Release\
  -DCMAKE_DISABLE_FIND_PACKAGE_LATEX=TRUE\
  -DCMAKE_DISABLE_DOCUMENTATION=TRUE -DINKSCAPE=FALSE\
  -DCMAKE_INSTALL_RPATH=/home/dedner/DUNEPIPA/dune-env/lib/\
  -DCMAKE_MACOSX_RPATH=TRUE -DCMAKE_BUILD_TYPE:STRING=Release
ninja install
cd ..
}

cd dune-typetree
build
cd ../dune-functions
build
cd ../dune-matrix-vector
build
cd ../dune-solvers
build
cd ../dune-tnnmg
build
cd ../dune-fufem
build
cd ..
