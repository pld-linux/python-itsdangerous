#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-itsdangerous.spec)

%define 	module  itsdangerous
Summary:	Various helpers to pass trusted data to untrusted environments and back
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niezaufanych środowisk
Name:		python-%{module}
# keep 1.x here for python2 support
Version:	1.1.0
Release:	4
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/itsdangerous
Source0:	https://pypi.python.org/packages/source/i/itsdangerous/%{module}-%{version}.tar.gz
# Source0-md5:	9b7f5afa7f1e3acfb7786eeca3d99307
URL:		http://github.com/mitsuhiko/itsdangerous
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-freezegun
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-freezegun
BuildRequires:	python3-pytest
%endif
%endif
%if %{with doc}
BuildRequires:	python-pallets-sphinx-themes >= 1.1.0
BuildRequires:	sphinx-pdg-2 >= 1.8.0
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Various helpers to pass data to untrusted environments and to get it
back safe and sound.

%description -l pl.UTF-8
Funkcje pomocnicze do przekazywania danych do niezaufanych środowisk i
pobierania ich w sposób bezpieczny.

%package -n python3-%{module}
Summary:	Various helpers to pass data to untrusted environments and to get it back safe and sound
Summary(pl.UTF-8):	Wspomaganie przekazywania danych do i z niebezpiecznych środowisk
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
Various helpers to pass data to untrusted environments and to get it
back safe and sound.

%description -n python3-%{module} -l pl.UTF-8
Funkcje pomocnicze do przekazywania danych do niezaufanych środowisk i
pobierania ich w sposób bezpieczny.

%package apidocs
Summary:	Documentation for Python itsdangerous module
Summary(pl.UTF-8):	Dokumentacja do moduły Pythona itsdangerous
Group:		Documentation

%description apidocs
Documentation for Python itsdangerous module.

%description apidocs -l pl.UTF-8
Dokumentacja do moduły Pythona itsdangerous.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%{py_sitescriptdir}/itsdangerous
%{py_sitescriptdir}/itsdangerous-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%{py3_sitescriptdir}/itsdangerous
%{py3_sitescriptdir}/itsdangerous-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
