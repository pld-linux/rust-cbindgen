# TODO: use shared crates?
Summary:	Tool for generating C bindings to Rust code
Summary(pl.UTF-8):	Narzędzie do generowania wiązań C do kodu w języku Rust
Name:		rust-cbindgen
Version:	0.9.1
Release:	1
License:	MPL v2.0
Group:		Development/Tools
#Source0Download: https://github.com/eqrion/cbindgen/releases
Source0:	https://github.com/eqrion/cbindgen/archive/v%{version}/cbindgen-%{version}.tar.gz
# Source0-md5:	36ec45a92f886fbec2e036bf70b13f21
# cd cbindgen-%{version}
# cargo vendor
# cd ..
# tar cJf cbindgen-crates-%{version}.tar.xz cbindgen-%{version}/{vendor,Cargo.lock}
Source1:	cbindgen-crates-%{version}.tar.xz
# Source1-md5:	9c4fb9275d15b30ead75a462c2a19f43
URL:		https://github.com/eqrion/cbindgen
BuildRequires:	cargo
BuildRequires:	rust
ExclusiveArch:	%{x8664} %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project can be used to generate C bindings for Rust code.

%description -l pl.UTF-8
Ten projekt służy do generowania wiązań C do kodu w języku Rust.

%prep
%setup -q -n cbindgen-%{version} -b1

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

cargo -v build --release --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

cargo -v install --frozen --root $RPM_BUILD_ROOT%{_prefix}
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates.toml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGES contributing.md docs.md internals.md
%attr(755,root,root) %{_bindir}/cbindgen
