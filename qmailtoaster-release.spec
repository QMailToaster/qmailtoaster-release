# $Id$
# Authority: shubes
# Upstream: Eric Shubert <eric@datamatters.us>

Name:      qmailtoaster-release
Summary:   QMailToaster RPM repository configuration
Version:   2.0
Release:   1%{?dist}
License:   GPL
Group:     System Environment/Base
URL:       http://qmailtoaster.com/
Packager:  Eric Shubert <qmt-build@datamatters.us>

Requires:  yum-priorities

Source1:   qt-whatami
Source2:   qmailtoaster.repo
Source3:   qmailtoaster-centos.repo
Source4:   qmailtoaster-fedora.repo
Source5:   qmailtoaster-mandriva.repo
Source6:   qmailtoaster-suse.repo
Source7:   RPM_GPG_KEY-qmailtoaster
Source8:   RPM_GPG_KEY-shubes

BuildArch: noarch
BuildRoot: %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define BASE_DIR   /opt/%{name}
%define BIN_DIR    %{BASE_DIR}/bin
%define CONF_DIR   %{BASE_DIR}/etc
%define BIN_LINK   %{_bindir}
%define REPO_LINK  %{_sysconfdir}/yum.repos.d

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
This package contains yum configuration files for the QMailToaster RPM
Repository, as well as the public GPG keys for verifying them.
It also includes a script for determining which distro the host is running,
to aid with installation and support.

#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------
%setup -cT

#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{BIN_DIR}
%{__mkdir_p} %{buildroot}%{CONF_DIR}
%{__mkdir_p} %{buildroot}%{BIN_LINK}
%{__mkdir_p} %{buildroot}%{REPO_LINK}

%{__install} -p %{_sourcedir}/qt-whatami \
                              %{buildroot}%{BIN_DIR}/qt-whatami

%{__install} -p %{_sourcedir}/qmailtoaster.repo \
                              %{buildroot}%{CONF_DIR}/qmailtoaster.repo
%{__install} -p %{_sourcedir}/qmailtoaster-centos.repo \
                              %{buildroot}%{CONF_DIR}/qmailtoaster-centos.repo
%{__install} -p %{_sourcedir}/qmailtoaster-fedora.repo \
                              %{buildroot}%{CONF_DIR}/qmailtoaster-fedora.repo
%{__install} -p %{_sourcedir}/qmailtoaster-mandriva.repo \
                              %{buildroot}%{CONF_DIR}/qmailtoaster-mandriva.repo
%{__install} -p %{_sourcedir}/qmailtoaster-suse.repo \
                              %{buildroot}%{CONF_DIR}/qmailtoaster-suse.repo

%{__install} -p %{_sourcedir}/RPM_GPG_KEY-qmailtoaster \
                              %{buildroot}%{CONF_DIR}/RPM_GPG_KEY-qmailtoaster
%{__install} -p %{_sourcedir}/RPM_GPG_KEY-shubes \
                              %{buildroot}%{CONF_DIR}/RPM_GPG_KEY-shubes

%{__ln_s} ../..%{BIN_DIR}/qt-whatami          %{buildroot}%{BIN_LINK}/.
%{__ln_s} ../..%{CONF_DIR}/qmailtoaster.repo  %{buildroot}%{REPO_LINK}/.
touch   %{buildroot}%{REPO_LINK}/qmailtoaster-dist.repo

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
%{__rm} -rf %{buildroot}

#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------
%defattr(0644, root, root, 0755)

# shubes - this is from repoforge-release - don't know what %pubkey does
# %pubkey RPM_GPG_KEY-qmailtoaster
# %pubkey RPM_GPG_KEY-shubes

# directories
%dir %{BASE_DIR}
%dir %{BIN_DIR}
%dir %{CONF_DIR}

# files
%attr(0755, root, root)  %{BIN_DIR}/*
%config(noreplace)       %{CONF_DIR}/*

# symlinks
%{BIN_LINK}/*
%{REPO_LINK}/qmailtoaster.repo
%ghost %{REPO_LINK}/qmailtoaster-dist.repo

#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------
. qt-whatami -s
case $DISTRO in
  CentOS )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-centos.repo \
           %{REPO_LINK}/qmailtoaster-dist.repo
    ;;
  Fedora )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-fedora.repo \
           %{REPO_LINK}/qmailtoaster-dist.repo
    ;;
  Mandriva )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-mandriva.repo \
           %{REPO_LINK}/qmailtoaster-dist.repo
    ;;
  SuSE )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-suse.repo \
           %{REPO_LINK}/qmailtoaster-dist.repo
    ;;
  * )
    echo "DISTRO not determined:"
    qt-whatami
    echo "ERROR: Please contact support"
    ;;
esac

rpm -q gpg-pubkey-4728f6b5-52900fa3 &>/dev/null || \
      rpm --import %{CONF_DIR}/RPM_GPG_KEY-qmailtoaster || :
rpm -q gpg-pubkey-93c761fd-528fd585 &>/dev/null || \
      rpm --import %{CONF_DIR}/RPM_GPG_KEY-shubes || :

co_parm="check_obsoletes=1"
pcfile=/etc/yum/pluginconf.d/priorities.conf
grep "$co_parm" $pcfile >/dev/null 2>&1 || \
      echo "$co_parm" >> $pcfile

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Sat Dec 07 2013 Eric Shubert <eric@datamatters.us> - 2.0-1.qt
* removed qt-install-repoforge from %post, as that won't work (recursive rpm)
- changed symlink name and made it a ghost
* Sat Nov 23 2013 Eric Shubert <eric@datamatters.us> - 2.0-0.qt
- Initial package.
