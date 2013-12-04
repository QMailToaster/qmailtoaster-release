# $Id$
# Authority: shubes
# Upstream: Eric Shubert <eric@datamatters.us>

Name:      qmailtoaster-release
Summary:   QMailToaster RPM repository configuration
Version:   2.0
Release:   0%{?dist}
License:   GPL
Group:     System Environment/Base
URL:       http://qmailtoaster.com/

Source0:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/qmt-whatami
Source1:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/qmt-install-repoforge
Source2:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/qmailtoaster.repo
Source3:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/qmailtoaster-centos.repo
Source4:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/qmailtoaster-fedora.repo
Source5:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/qmailtoaster-mandriva.repo
Source6:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/qmailtoaster-suse.repo
Source7:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/RPM_GPG_KEY-qmailtoaster
Source8:   https://raw.github.com/QMailToaster/pkgs/master/%{name}/RPM_GPG_KEY-shubes

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

%{__install} -p %{SOURCE0} %{buildroot}%{BIN_DIR}/qmt-whatami
%{__install} -p %{SOURCE1} %{buildroot}%{BIN_DIR}/qmt-install-repoforge

%{__install} -p %{SOURCE2} %{buildroot}%{CONF_DIR}/qmailtoaster.repo
%{__install} -p %{SOURCE3} %{buildroot}%{CONF_DIR}/qmailtoaster-centos.repo
%{__install} -p %{SOURCE4} %{buildroot}%{CONF_DIR}/qmailtoaster-fedora.repo
%{__install} -p %{SOURCE5} %{buildroot}%{CONF_DIR}/qmailtoaster-mandriva.repo
%{__install} -p %{SOURCE6} %{buildroot}%{CONF_DIR}/qmailtoaster-suse.repo

%{__install} -p %{SOURCE7} %{buildroot}%{CONF_DIR}/RPM_GPG_KEY-qmailtoaster
%{__install} -p %{SOURCE8} %{buildroot}%{CONF_DIR}/RPM_GPG_KEY-shubes

%{__ln_s} ../..%{BIN_DIR}/qmt-whatami            %{buildroot}%{BIN_LINK}/.
%{__ln_s} ../..%{BIN_DIR}/qmt-install-repoforge  %{buildroot}%{BIN_LINK}/.
%{__ln_s} ../..%{CONF_DIR}/qmailtoaster.repo     %{buildroot}%{REPO_LINK}/.

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
%{__rm} -rf %{buildroot}

#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------
%defattr(0644, root, root, 0755)

# shubes - this is from rpmforge-release - don't know what %pubkey does
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
%{REPO_LINK}/*

#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------
. qmt-whatami -s
case $DISTRO in
  CentOS )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-centos.repo   %{REPO_LINK}/.
    qmt-install-repoforge
    ;;
  Fedora )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-fedora.repo   %{REPO_LINK}/.
    ;;
  Mandriva )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-mandriva.repo %{REPO_LINK}/.
    ;;
  SuSE )
    %{__ln_s} ../..%{CONF_DIR}/qmailtoaster-suse.repo     %{REPO_LINK}/.
    ;;
  * )
    echo "DISTRO not determined:"
    qmt-whatami
    echo "ERROR: Please contact support"
    ;;
esac

rpm -q gpg-pubkey-4728f6b5-52900fa3 &>/dev/null || \
      rpm --import %{CONF_DIR}/RPM_GPG_KEY-qmailtoaster || :
rpm -q gpg-pubkey-93c761fd-528fd585 &>/dev/null || \
      rpm --import %{CONF_DIR}/RPM_GPG_KEY-shubes || :

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Sat Nov 23 2013 Eric Shubert <eric@datamatters.us> - 2.0-0.qt
- Initial package.