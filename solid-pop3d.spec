#
# Conditional build:
%bcond_without	apop	# build without APOP support
%bcond_without	ipv6	# build without IPv6 support
%bcond_without	maildir	# build without Maildir support
%bcond_with	sasl	# build with SASL support (uses obsolete cyrus-sasl 1.x)
%bcond_without	ssl	# build without SSL support
%bcond_with	standalone	# compile server as a standalone server, not inetd
%bcond_with	whoson	# build with whoson support
#
Summary:	POP3 server
Summary(pl.UTF-8):	Serwer POP3
Name:		solid-pop3d
Version:	0.16d
Release:	14
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://dione.ids.pl/pub/solidpop3d/%{name}-%{version}.tar.gz
# Source0-md5:	ad197a3cf8310994f2fad90376edbd91
Source1:	%{name}.conf
Source2:	%{name}-ssl.conf
Source3:	%{name}.inetd
Source4:	%{name}-ssl.inetd
Source5:	%{name}.pamd
Patch0:		%{name}-whoson2.patch
Patch1:		%{name}-user.patch
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_sasl:BuildRequires:	cyrus-sasl-devel < 2.0.0}
BuildRequires:	gdbm-devel
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_whoson:BuildRequires:	whoson-devel}
Requires:	pam >= 0.79.0
%{?with_standalone:Requires:	rc-inetd >= 0.8.1}
Provides:	pop3daemon
Provides:	user(pop3)
Obsoletes:	imap-pop
Obsoletes:	qpopper
Obsoletes:	qpopper6
Obsoletes:	solid-pop3d-ssl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Solid POP3 Server is an implementation of a Post Office Protocol
version 3 server that has flexibility as its main goal. The server is
easily configurable and has support for few features such as:
- APOP authentication scheme
- virtual hosting
- maildir and mailbox handling
- bulletins
- expiration of messages

%description -l pl.UTF-8
Serwer Solid POP3 jest implementacją protokołu Post Office Protocol w
wersji 3 mający za główny cel elastyczność. Serwer jest łatwo
konfigurowalny oraz posiada wsparcie dla wielu nowinek takich jak:
- schemat autoryzacji APOP
- wirtualne serwery
- formaty maildir oraz mailbox skrzynek pocztowych
- obsługa biuletynów
- obsługa przeterminowywania się wiadomości

%prep
%setup -q
cp -f /usr/share/automake/config.sub .
%{?with_whoson:%patch0 -p1}
%patch1 -p1

%build
%{__autoheader}
%{__autoconf}
%configure \
	--localstatedir=/var/mail \
	--enable-pam \
	%{?with_apop:--enable-apop} \
	--enable-mailbox \
	%{!?with_maildir:--disable-maildir} \
	--disable-crlfmaildir \
	--enable-bulletins \
	--enable-expire \
	--enable-configfile \
	--enable-userconfig \
	%{?with_standalone:--enable-standalone} \
	--enable-last \
	--enable-mapping \
	--enable-nonip \
	--disable-allowroot \
	--enable-createmail \
	%{?with_ipv6:--enable-ipv6} \
	--disable-resolve \
	--disable-connect \
	--enable-logextend \
	--enable-statistics \
	--enable-dpuid \
	--enable-userpasswd \
	--enable-hashspool \
	--enable-authonly \
	%{?with_ssl:--with-openssl} \
	%{?with_whoson:--enable-whoson} \
	%{?with_sasl:--with-sasl}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,%{!?with_standalone:sysconfig/rc-inetd,}security} \
	$RPM_BUILD_ROOT/var/mail/bulletins

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/spop3d.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/spop3d-ssl.conf
%{!?with_standalone:install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/spop3d}
%{!?with_standalone:install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/spop3d-ssl}
install %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/spop3d

touch $RPM_BUILD_ROOT%{_sysconfdir}/security/blacklist.spop3d

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 60 -r -d /var/mail/bulletins -s /bin/false -c "pop3 user" -g nobody pop3

%post
%{!?with_standalone:%service -q rc-inetd reload}

%postun
if [ "$1" = 0 ]; then
	%{!?with_standalone:%service -q rc-inetd reload}
	%userremove pop3
fi

%triggerpostun -- solid-pop3d < 0.16d-8
if [ "$1" != "0" ]; then
	%userremove spop3d
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README SASL THANKS TLS VIRTUALS doc/config.example
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%{!?with_standalone:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/spop3d}
%{!?with_standalone:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/spop3d-ssl}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.spop3d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/spop3d
%attr(640,pop3,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/spop3d.conf
%attr(640,pop3,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/spop3d-ssl.conf
%attr(755,root,root) %dir /var/mail/bulletins
%{_mandir}/man[158]/*
