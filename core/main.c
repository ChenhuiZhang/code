#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <inttypes.h>
#include <unistd.h>
#include <fcntl.h>
#include <curl/curl.h>
#include <syslog.h>
#include <sys/socket.h>
#include <sys/un.h>

#define CORED_MGM_PATH "/var/run/dbg-cgi/ctrl-segf-socket"

#define D(x)

int cored_mgm_connect(void)
{
	int err;
	int fd;
	struct sockaddr_un saddr;
	
	memset(&saddr, 0, sizeof saddr );
	saddr.sun_family = AF_UNIX;
	memcpy(&saddr.sun_path, 
	       CORED_MGM_PATH, strlen(CORED_MGM_PATH));

	fd = socket (AF_UNIX, SOCK_STREAM, 0);
	if (fd == -1)
		return -1;

	err = connect (fd, (struct sockaddr *) &saddr, sizeof saddr);
	if (err == -1) {
		fprintf (stderr, "connect to %s failed\n", 
			 CORED_MGM_PATH);
		close (fd);
		fd = -1;
	}
	return fd;
}

void cored_mgm_close(int fd)
{
	char buf[8];
	fd_set rfds;
	struct timeval tv;
	int r;

	/* Watch fd to see when it has input. */
	FD_ZERO(&rfds);
	FD_SET(fd, &rfds);

	/* Wait up to five seconds. */
	tv.tv_sec = 5;
	tv.tv_usec = 0;

	r = select(fd + 1, &rfds, NULL, NULL, &tv);
	/* Don't rely on the value of tv now! */

	if (r == -1)
		perror("select()");
	else if (r) 
		r = read (fd, &buf, sizeof buf);
	close (fd);
}

static size_t stdin_read_callback(void *ptr, size_t size, size_t nmemb, void *stream)
{
	ssize_t retcode = read(0, ptr, size * nmemb);
	if (retcode < 0) {
		D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__,
		__LINE__, retcode));
		return CURL_READFUNC_ABORT;
	}

	return (size_t)retcode;
}

static int ftp_upload_core(int argc, const char **argv)
{
	CURL *curl;
	CURLcode res;
	int retcode = EXIT_FAILURE;
	struct curl_slist *headerlist = NULL;
	char* ftp_command = NULL;
	char* remote_target = NULL;

	/* Configuration */
	struct std2parser_cfg *retval;
	char* target_url = "ftp://root:pass@192.168.77.132:21";
	char* target_path = "/tmp";
	const char* target_file = "core.core";
	long timeout = 0;

	if (argc > 1) {
		target_file = argv[1];
	}

	/* Build remote target string */
	if (asprintf(&remote_target, "%s%s/%s", target_url, target_path, target_file) == -1) {
		D(fprintf(stderr, "Error allocating memory for remote_target\n"));
		syslog(LOG_INFO, "1");
		goto error;
	}
	/* Build ftp command string */
	if (asprintf(&ftp_command, "RNFR %s/%s", target_path, target_file) == -1) {
		D(fprintf(stderr, "Error allocating memory for remote_target\n"));
		syslog(LOG_INFO, "2");
		goto error;
	}

	/* Init curl */
	res = curl_global_init(CURL_GLOBAL_ALL);
	if (res != CURLE_OK) {
		D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__, __LINE__, res));
		syslog(LOG_INFO, "3");
		goto error;
	}

	/* Get a curl handle */
	curl = curl_easy_init();
	if(curl) {
		/* build a list of commands to pass to libcurl */
		headerlist = curl_slist_append(headerlist, ftp_command);

		/* Set read function to read from stdin */
		res = curl_easy_setopt(curl, CURLOPT_READFUNCTION,
				stdin_read_callback);
		if (res != CURLE_OK) {
			D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__,
				__LINE__, res));
		  syslog(LOG_INFO, "4");
			goto ftp_error;
		}

		/* Enable uploading */
		res = curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
		if (res != CURLE_OK) {
			D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__,
				__LINE__, res));
			goto ftp_error;
		}

		/* Specify target */
		syslog(LOG_INFO, "remote_target: %s\n", remote_target);
		res = curl_easy_setopt(curl, CURLOPT_URL, remote_target);
		if (res != CURLE_OK) {
			D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__,
				__LINE__, res));
			goto ftp_error;
		}

		/* Set FTP commands */
		res = curl_easy_setopt(curl, CURLOPT_POSTQUOTE, headerlist);
		if (res != CURLE_OK) {
			D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__,
				__LINE__, res));
			goto ftp_error;
		}

		/* Set connection timeout */
		res = curl_easy_setopt(curl, CURLOPT_TIMEOUT, timeout);
		if (res != CURLE_OK) {
			D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__,
				__LINE__, res));
			goto ftp_error;
		}

		/* Upload */
		syslog(LOG_INFO, "Upload ....\n");
		res = curl_easy_perform(curl);
		if (res != CURLE_OK) {
			D(fprintf(stderr, "%s:%d %d\n", __FUNCTION__,
				__LINE__, res));
		  syslog(LOG_INFO, "curl_easy_perform\n");
			if (res == CURLE_OPERATION_TIMEDOUT) {
				syslog(LOG_WARNING, "coredump truncated.");
			}
			goto ftp_error;
		} else {
			retcode = EXIT_SUCCESS;
		}
	}

ftp_error:
	/* Cleanup */
	curl_slist_free_all (headerlist);
	curl_easy_cleanup(curl);
	curl_global_cleanup();
error:
	free (ftp_command);
	free (remote_target);

	return retcode;
}

int main(int argc, const char *argv[])
{
  int h;
  printf("Hello, core!\n");

  openlog(NULL, LOG_PID, LOG_USER);
  syslog(LOG_INFO, "Hello, core!\n");

#if 0
  h = cored_mgm_connect();
  if (h < 0) {
  } else {
    safe_copyfd(0, h);
    cored_mgm_close(h);
  }
#else
  ftp_upload_core(argc, argv);
#endif

  closelog();
  return 0;
}
