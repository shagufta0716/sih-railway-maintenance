import { exec } from 'child_process';
import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function POST() {
  return new Promise((resolve) => {
    // Run python scheduler.py --source real in the root directory
    exec('python scheduler.py', { cwd: '../backend/' }, (error, stdout, stderr) => {
      if (error) {
        resolve(NextResponse.json({ error: error.message, stderr }, { status: 500 }));
      } else {
        resolve(NextResponse.json({ success: true, stdout }));
      }
    });
  });
}
