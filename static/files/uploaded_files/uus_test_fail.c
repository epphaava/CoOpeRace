#include <pthread.h>
#include <stdio.h>

int myglobal1;
int myglobal2;
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex2 = PTHREAD_MUTEX_INITIALIZER;

void *t_fun(void *arg) {
  pthread_mutex_lock(&mutex1);
  myglobal1=myglobal1+1; // RACE!
  myglobal2=myglobal2+1; // RACE!
  pthread_mutex_unlock(&mutex1);
  return NULL;
}

int main(void) {
  pthread_t id;
  pthread_create(&id, NULL, t_fun, NULL);
  pthread_mutex_lock(&mutex2);
  myglobal1=myglobal1+1; // RACE!
  myglobal2=myglobal2+1; // RACE!
  pthread_mutex_unlock(&mutex2);
  pthread_join (id, NULL);
  return 0;
}