/**
 * Mobile Offline Scan Queue Manager
 * Stores captured scans locally when offline and synchronizes automatically upon reconnect.
 */

export interface PendingScan {
  id: string;
  imageUri: string;
  isRuralSetting: boolean;
  capturedAt: string;
}

class OfflineQueueManager {
  private queue: PendingScan[] = [];

  public enqueueScan(scan: PendingScan) {
    this.queue.push(scan);
    console.log(`[OfflineQueue] Enqueued scan ${scan.id}. Total pending: ${this.queue.length}`);
  }

  public getPendingQueue(): PendingScan[] {
    return this.queue;
  }

  public async syncQueue(uploadApi: (scan: PendingScan) => Promise<boolean>): Promise<number> {
    let syncedCount = 0;
    const remaining: PendingScan[] = [];

    for (const scan of this.queue) {
      try {
        const success = await uploadApi(scan);
        if (success) {
          syncedCount++;
        } else {
          remaining.push(scan);
        }
      } catch (err) {
        remaining.push(scan);
      }
    }

    this.queue = remaining;
    console.log(`[OfflineQueue] Sync completed. Synced: ${syncedCount}, Remaining: ${this.queue.length}`);
    return syncedCount;
  }
}

export const offlineQueue = new OfflineQueueManager();
