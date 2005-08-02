# $Id$

Name: pdsh   
Version: 2.5
Release: 1

Summary: Parallel remote shell program.

License: GPL
Group: System Environment/Base
Source: 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
Requires: pdsh-rcmd


#
# If "--with debug" is set compile with --enable-debug
#   and try not to strip binaries.
#
# (See /usr/share/doc/rpm-*/conditionalbuilds)
#
%if %{?_with_debug:1}%{!?_with_debug:0}
  %define _enable_debug --enable-debug
  %define __os_install_post /usr/lib/rpm/brp-compress
%endif

#
# Enabling and disabling pdsh options
#  defaults:
#  enabled:  readline, rsh, ssh
#  disabled: rms, mrsh, qshell, mqshell, genders, nodeattr, machines,
#            nodeupdown

#  To build the various module subpackages, pass --with <pkg> on
#   the rpmbuild command line (if your rpm is a recent enough version)
#  
#  Similarly, to disable various pdsh options pass --without <pkg> on
#   the rpmbuild command line.
#

# readline, rsh, and ssh are built by default:
#
%{!?_with_readline: %{!?_without_readline: %define _with_readline --with-readline}}
%{!?_with_rsh: %{!?_without_rsh: %define _with_rsh 1}}
%{!?_with_ssh: %{!?_without_ssh: %define _with_ssh --with-ssh}}

# everything else is disabled
#
%{!?_without_rms: %{!?_with_rms: %define _without_rms --without-rms}}
%{!?_without_slurm: %{!?_with_slurm: %define _without_slurm --without-slurm}}
%{!?_without_mrsh: %{!?_with_mrsh: %define _without_mrsh --without-mrsh}}
%{!?_without_qshell: %{!?_with_qshell: %define _without_qshell --without-qshell}}
%{!?_without_mqshell: %{!?_with_mqshell: %define _without_mqshell --without-mqshell}}
%{!?_without_genders: %{!?_with_genders: %define _without_genders --without-genders}}
%{!?_without_nodeattr: %{!?_with_nodeattr: %define _without_nodeattr --without-nodeattr}}
%{!?_without_machines: %{!?_with_machines: %define _without_machines --without-machines}}
%{!?_without_nodeupdown: %{!?_with_nodeupdown: %define _without_nodeupdown --without-nodeupdown}}

%{?_with_qshell:BuildRequires: qsnetlibs}
%{?_with_mqshell:BuildRequires: qsnetlibs}
%{?_with_readline:BuildRequires: readline-devel}
%{?_with_nodeupdown:BuildRequires: whatsup}
%{?_with_genders:BuildRequires: genders > 1.0}

##############################################################################
# Pdsh description

%description
Pdsh is a multithreaded remote shell client which executes commands
on multiple remote hosts in parallel.  Pdsh can use several different
remote shell services, including standard "rsh", Kerberos IV, and ssh.
##############################################################################

%package qshd
Summary: Remote shell daemon for pdsh/qshell/Elan3
Group:   System Environment/Base
Prereq:  xinetd
%description qshd
Remote shell service for running Quadrics Elan3 jobs under pdsh.
Sets up Elan capabilities and environment variables needed by Quadrics
MPICH executables.
##############################################################################

%package mqshd
Summary: Remote shell daemon for pdsh/mqshell/Elan3
Group:   System Environment/Base
Prereq:  xinetd
%description mqshd
Remote shell service for running Quadrics Elan3 jobs under pdsh with
mrsh authentication.  Sets up Elan capabilities and environment variables 
needed by Quadrics MPICH executables.
##############################################################################

#
# Module packages:
#
%package   rcmd-rsh
Summary:   Provides bsd rcmd capability to pdsh.
Group:     System Environment/Base
Provides:  pdsh-rcmd
%description rcmd-rsh
Pdsh module for bsd rcmd functionality. Note: This module
requires that the pdsh binary be installed setuid root.

%package   rcmd-ssh
Summary:   Provides ssh rcmd capability to pdsh.
Group:     System Environment/Base
Provides:  pdsh-rcmd
%description rcmd-ssh
Pdsh module for ssh rcmd functionality.

%package   rcmd-qshell
Summary:   Provides qshell rcmd capability to pdsh.
Group:     System Environment/Base
Provides:  pdsh-rcmd
Conflicts: pdsh-rcmd-mqshell
%description rcmd-qshell
Pdsh module for running QsNet MPI jobs. Note: This module
requires that the pdsh binary be installed setuid root.

%package   rcmd-mrsh
Summary:   Provides mrsh rcmd capability to pdsh.
Group:     System Environment/Base
Provides:  pdsh-rcmd
%description rcmd-mrsh
Pdsh module for mrsh rcmd functionality.

%package   rcmd-mqshell
Summary:   Provides mqshell rcmd capability to pdsh.
Group:     System Environment/Base
Provides:  pdsh-rcmd
Conflicts: pdsh-rcmd-qshell
%description rcmd-mqshell
Pdsh module for mqshell rcmd functionality.

%package   mod-genders
Summary:   Provides libgenders support for pdsh.
Group:     System Environment/Base
Requires:  genders >= 1.1
Conflicts: pdsh-mod-nodeattr
Conflicts: pdsh-mod-machines
%description mod-genders
Pdsh module for libgenders functionality.

%package   mod-nodeattr
Summary:   Provides genders support for pdsh using the nodeattr program.
Group:     System Environment/Base
Requires:  genders 
Conflicts: pdsh-mod-genders
Conflicts: pdsh-mod-machines
%description mod-nodeattr
Pdsh module for genders functionality using the nodeattr program.

%package   mod-nodeupdown
Summary:   Provides libnodeupdown support for pdsh.
Group:     System Environment/Base
Requires:  whatsup
%description mod-nodeupdown
Pdsh module providing -v functionality using libnodeupdown.

%package   mod-rms
Summary:   Provides RMS support for pdsh.
Group:     System Environment/Base
Requires:  qsrmslibs
%description mod-rms
Pdsh module providing support for gathering the list of target nodes
from an allocated RMS resource.

%package   mod-machines
Summary:   Pdsh module for gathering list of target nodes from a machines file.
Group:     System Environment/Base
Conflicts: pdsh-mod-genders
Conflicts: pdsh-mod-nodeattr
%description mod-machines
Pdsh module for gathering list of all target nodes from a machines file.

%package   mod-slurm
Summary:   Provides support for running pdsh under SLURM allocations.
Group:     System Environment/Base
Requires:  slurm
%description mod-slurm
Pdsh module providing support for gathering the list of target nodes
from an allocated SLURM job.



##############################################################################

%prep
%setup -n %{name}-%{version}-%{release}
##############################################################################

%build
%configure --program-prefix=%{?_program_prefix:%{_program_prefix}} \
    %{?_enable_debug}       \
    %{?_with_rsh}           \
    %{?_without_rsh}        \
    %{?_with_ssh}           \
    %{?_without_ssh}        \
    %{?_with_qshell}        \
    %{?_without_qshell}     \
    %{?_with_readline}      \
    %{?_without_readline}   \
    %{?_with_machines}      \
    %{?_without_machines}   \
    %{?_with_genders}       \
    %{?_without_genders}    \
    %{?_with_rms}           \
    %{?_without_rms}        \
    %{?_with_nodeupdown}    \
    %{?_without_nodeupdown} \
    %{?_with_nodeattr}      \
    %{?_without_nodeattr}   \
    %{?_with_mrsh}          \
    %{?_without_mrsh}       \
    %{?_with_mqshell}       \
    %{?_without_mqshell}    \
    %{?_with_slurm}         \
    %{?_without_slurm}        
    
           
if [ "$SMP" != "" ] ; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi
##############################################################################

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
DESTDIR="$RPM_BUILD_ROOT" make install
if [ -x $RPM_BUILD_ROOT/%{_sbindir}/in.qshd ]; then
   install -D -m644 etc/qshell.xinetd $RPM_BUILD_ROOT/etc/xinetd.d/qshell
fi
if [ -x $RPM_BUILD_ROOT/%{_sbindir}/in.mqshd ]; then
   install -D -m644 etc/mqshell.xinetd $RPM_BUILD_ROOT/etc/xinetd.d/mqshell
fi

##############################################################################

%clean
rm -rf "$RPM_BUILD_ROOT"
##############################################################################

%files
%defattr(-,root,root)
%doc README ChangeLog NEWS DISCLAIMER README.KRB4 README.modules README.QsNet
%attr(755, root, root) %{_bindir}/pdsh
%attr(755, root, root) %{_bindir}/pdcp
%{_bindir}/dshbak
%{_mandir}/man1/*
##############################################################################

%if %{?_with_rsh:1}%{!?_with_rsh:0}
%files rcmd-rsh
%defattr(-,root,root)
%{_libdir}/pdsh/xrcmd.*
%endif
##############################################################################

%if %{?_with_ssh:1}%{!?_with_ssh:0}
%files rcmd-ssh
%defattr(-,root,root)
%{_libdir}/pdsh/sshcmd.*
%endif
##############################################################################

%if %{?_with_qshell:1}%{!?_with_qshell:0}
%files rcmd-qshell
%defattr(-,root,root)
%{_libdir}/pdsh/qcmd.*
%endif
##############################################################################

%if %{?_with_mrsh:1}%{!?_with_mrsh:0}
%files rcmd-mrsh
%defattr(-,root,root)
%{_libdir}/pdsh/mcmd.*
%endif
##############################################################################

%if %{?_with_mqshell:1}%{!?_with_mqshell:0}
%files rcmd-mqshell
%defattr(-,root,root)
%{_libdir}/pdsh/mqcmd.*
%endif
##############################################################################

%if %{?_with_genders:1}%{!?_with_genders:0}
%files mod-genders
%defattr(-,root,root)
%{_libdir}/pdsh/genders.*
%endif
##############################################################################

%if %{?_with_nodeattr:1}%{!?_with_nodeattr:0}
%files mod-nodeattr
%defattr(-,root,root)
%{_libdir}/pdsh/nodeattr.*
%endif
##############################################################################

%if %{?_with_nodeupdown:1}%{!?_with_nodeupdown:0}
%files mod-nodeupdown
%defattr(-,root,root)
%{_libdir}/pdsh/nodeupdown.*
%endif
##############################################################################

%if %{?_with_rms:1}%{!?_with_rms:0}
%files mod-rms
%defattr(-,root,root)
%{_libdir}/pdsh/rms.*
%endif
##############################################################################

%if %{?_with_machines:1}%{!?_with_machines:0}
%files mod-machines
%defattr(-,root,root)
%{_libdir}/pdsh/machines.*
%endif
##############################################################################

%if %{?_with_slurm:1}%{!?_with_slurm:0}
%files mod-slurm
%defattr(-,root,root)
%{_libdir}/pdsh/slurm.*
%endif
##############################################################################

%if %{?_with_qshell:1}%{!?_with_qshell:0}
%files qshd
%defattr(-,root,root)
%{_sbindir}/in.qshd
/etc/xinetd.d/qshell

%post qshd
if ! grep "^qshell" /etc/services >/dev/null; then
  echo "qshell            523/tcp                  # pdsh/qshell/elan3" >>/etc/services
fi
/etc/init.d/xinetd reload

%endif
##############################################################################

%if %{?_with_mqshell:1}%{!?_with_mqshell:0}
%files mqshd
%defattr(-,root,root)
%{_sbindir}/in.mqshd
/etc/xinetd.d/mqshell

%post mqshd
if ! grep "^mqshell" /etc/services >/dev/null; then
  echo "mqshell         21234/tcp                  # pdsh/mqshell/elan3" >>/etc/services
fi
/etc/init.d/xinetd reload

%endif
##############################################################################

%post
rm -f /var/cache/man/cat1/pdsh.1.*
rm -f /var/cache/man/cat1/pdcp.1.*