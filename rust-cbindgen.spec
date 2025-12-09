# TODO: use shared crates?
%define		crates_ver	0.29.2

Summary:	Tool for generating C bindings to Rust code
Summary(pl.UTF-8):	Narzędzie do generowania wiązań C do kodu w języku Rust
Name:		rust-cbindgen
Version:	0.29.2
Release:	1
License:	MPL v2.0
Group:		Development/Tools
#Source0Download: https://github.com/eqrion/cbindgen/releases
Source0:	https://github.com/eqrion/cbindgen/archive/v%{version}/cbindgen-%{version}.tar.gz
# Source0-md5:	5da43d9d5547eb1abdd63eb11482eb7e
# cd cbindgen-%{version}
# cargo vendor
# cd ..
# tar cJf cbindgen-crates-%{version}.tar.xz cbindgen-%{version}/{vendor,Cargo.lock}
Source1:	cbindgen-crates-%{crates_ver}.tar.xz
# Source1-md5:	45b84a2b27d6c5f722313a6a72d9b5fa
URL:		https://github.com/eqrion/cbindgen
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.74
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project can be used to generate C bindings for Rust code.

%description -l pl.UTF-8
Ten projekt służy do generowania wiązań C do kodu w języku Rust.

%prep
%setup -q -n cbindgen-%{version} -a1

%{__mv} cbindgen-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGES contributing.md docs.md internals.md
%attr(755,root,root) %{_bindir}/cbindgen
